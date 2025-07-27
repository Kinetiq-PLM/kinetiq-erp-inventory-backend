from rest_framework import generics, viewsets, status
from .models import CyclicCount, InventoryItem, Product, ItemMasterData, InventoryItemThreshold
from .serializers import (
    CyclicCountSerializer, ProductSerializer, ItemMasterDataSerializer, 
    InventoryItemThresholdSerializer, InventoryItemSerializer
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
import logging
from django.apps import apps
from django.db import connection

logger = logging.getLogger(__name__)

class CyclicCountList(APIView):
    def get(self, request):
        try:
            # Add back select_related to fetch the related inventory item efficiently
            cyclic_counts = CyclicCount.objects.select_related('inventory_item').all()
            serializer = CyclicCountSerializer(cyclic_counts, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching cyclic counts: {str(e)}")
            return Response({"error": "Failed to fetch cyclic counts"}, status=500)

    def post(self, request):
        try:
            serializer = CyclicCountSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            logger.error(f"Error creating cyclic count: {str(e)}")
            return Response({"error": "Failed to create cyclic count"}, status=500)

class WarehouseList(APIView):
    """
    View to list all available warehouse IDs and locations.
    Returns data in the format: [{'warehouse_id': id, 'warehouse_location': name}, ...]
    """
    def get(self, request):
        try:
            warehouse_data = []
            
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT warehouse_id, warehouse_location 
                    FROM admin.warehouse
                    ORDER BY warehouse_location, warehouse_id
                    """
                )
                rows = cursor.fetchall()
                
                for row in rows:
                    warehouse_id = row[0]
                    # Use location if available, otherwise fallback to id as name
                    warehouse_location = row[1] if row[1] else row[0] 
                    warehouse_data.append({
                        'warehouse_id': warehouse_id,
                        'warehouse_location': warehouse_location
                    })
            
            # Fallback if admin.warehouse query returns nothing (optional, based on requirements)
            if not warehouse_data:
                warehouse_ids = InventoryItem.objects.values_list('warehouse_id', flat=True).distinct()
                # Create list with id and name (using id as name if location isn't available)
                warehouse_data = [{'warehouse_id': w, 'warehouse_location': w} for w in warehouse_ids if w]
                # Optionally sort this fallback list as well
                warehouse_data.sort(key=lambda x: x['warehouse_location']) 

            return Response(warehouse_data)
        except Exception as e:
            logger.error(f"Error fetching warehouse list: {str(e)}")
            return Response({"error": "Failed to fetch warehouse list"}, status=500)

class InventoryItemList(APIView):
    """
    View to list all inventory items.
    """
    def get(self, request):
        try:
            inventory_items = InventoryItem.objects.all()
            serializer = InventoryItemSerializer(inventory_items, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching inventory items: {str(e)}")
            return Response({"error": "Failed to fetch inventory items"}, status=500)

class NotificationViewSet(viewsets.ViewSet):
    """
    A viewset for handling inventory discrepancy notifications.
    This creates entries in the admin.notifications table.
    """
    
    def create(self, request):
        """
        Create a new notification for an inventory discrepancy.
        
        Required fields:
        - module: String identifier for the source module (e.g., "INVENTORY")
        - to_user_id: User ID of the recipient
        - message: The notification message content
        - notifications_status: Status of the notification (e.g., "Unread")
        """
        try:
            # Extract required fields from request data
            module = request.data.get('module')
            to_user_id = request.data.get('to_user_id')
            message = request.data.get('message')
            notifications_status = request.data.get('notifications_status', 'Unread')
            
            # Validate required fields
            if not all([module, to_user_id, message]):
                return Response(
                    {"error": "Missing required fields. Please provide module, to_user_id, and message."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Execute raw SQL to insert into the admin.notifications table
            # This is a direct approach since we don't have a Django model for this table
            with connection.cursor() as cursor:
                # The table uses a trigger to generate the notifications_id
                cursor.execute(
                    """
                    INSERT INTO admin.notifications 
                    (module, to_user_id, message, notifications_status) 
                    VALUES (%s, %s, %s, %s) 
                    RETURNING notifications_id
                    """, 
                    [module, to_user_id, message, notifications_status]
                )
                
                # Get the generated notification ID
                result = cursor.fetchone()
                notification_id = result[0] if result else None
            
            # Return success response with the created notification ID
            return Response({
                "success": True,
                "message": "Notification created successfully",
                "notification_id": notification_id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # Handle any exceptions
            logger.error(f"Error creating notification: {str(e)}")
            return Response(
                {"error": f"Failed to create notification: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Add UserList API view
class UserList(APIView):
    """
    View to list all available admin users.
    """
    def get(self, request):
        try:
            # Use direct DB connection to fetch users and their roles
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT u.user_id, u.first_name, u.last_name, u.employee_id, r.role_name 
                    FROM admin.users u
                    LEFT JOIN admin.roles_permission r ON u.role_id = r.role_id
                    ORDER BY u.first_name, u.last_name
                    """
                )
                rows = cursor.fetchall()
                
                # Format as list of objects
                users = []
                for row in rows:
                    users.append({
                        'user_id': row[0],
                        'name': f"{row[1]} {row[2]}",  # Combine first_name and last_name
                        'employee_id': row[3],
                        'role_name': row[4] if row[4] else 'N/A' # Handle cases where role might be null
                    })
                
                return Response(users)
        except Exception as e:
            logger.error(f"Error fetching users: {str(e)}")
            return Response({"error": f"Failed to fetch users: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CyclicCountStatusUpdate(APIView):
    """
    View to update the status of a cyclic count.
    Ensures proper status transitions: Open -> In Progress -> Completed -> Closed
    """
    
    def get_valid_transitions(self, current_status):
        """
        Define valid status transitions based on current status
        """
        transitions = {
            'Open': ['In Progress', 'Cancelled'],
            'In Progress': ['Completed', 'Cancelled'],
            'Completed': ['Closed', 'In Progress'],  # Allow reopening if needed
            'Closed': [],  # Terminal state, no further transitions
            'Cancelled': []  # Terminal state, no further transitions
        }
        return transitions.get(current_status, [])
    
    def patch(self, request, count_id):
        try:
            # Get the cyclic count instance
            cyclic_count = get_object_or_404(CyclicCount, inventory_count_id=count_id)
            
            # Get the current and new status
            current_status = cyclic_count.status
            new_status = request.data.get('status')
            
            # Validate status is provided
            if not new_status:
                return Response(
                    {"error": "Status field is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if the transition is valid
            valid_transitions = self.get_valid_transitions(current_status)
            if not valid_transitions and current_status != new_status:
                return Response(
                    {"error": f"No transitions allowed from '{current_status}' status"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if new_status not in valid_transitions and current_status != new_status:
                return Response(
                    {"error": f"Invalid status transition from '{current_status}' to '{new_status}'. Valid transitions are: {', '.join(valid_transitions)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Optional: Get remarks for status change
            remarks = request.data.get('remarks')
            if remarks:
                cyclic_count.remarks = remarks
            
            # Update the status
            cyclic_count.status = new_status
            cyclic_count.save()
            
            # Return the updated cyclic count
            serializer = CyclicCountSerializer(cyclic_count)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error updating cyclic count status: {str(e)}")
            return Response(
                {"error": f"Failed to update status: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
