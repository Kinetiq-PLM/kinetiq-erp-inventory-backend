from rest_framework import generics, viewsets, status
from .models import CyclicCount, InventoryItem, Product, ItemMasterData, InventoryItemThreshold, Employee
from .serializers import (
    CyclicCountSerializer, ProductSerializer, ItemMasterDataSerializer, 
    InventoryItemThresholdSerializer, EmployeeSerializer, InventoryItemSerializer
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
            cyclic_counts = CyclicCount.objects.all()
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
    View to list all available warehouse IDs.
    """
    def get(self, request):
        try:
            # Query distinct warehouse IDs from inventory items
            warehouse_ids = InventoryItem.objects.values_list('warehouse_id', flat=True).distinct()
            
            # Convert to list and filter out None values
            warehouse_list = [w for w in warehouse_ids if w]
            
            return Response(warehouse_list)
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
            # Use direct DB connection to fetch users
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT user_id, first_name, last_name 
                    FROM admin.users
                    ORDER BY first_name, last_name
                    """
                )
                rows = cursor.fetchall()
                
                # Format as list of objects with id and name
                users = []
                for row in rows:
                    users.append({
                        'user_id': row[0],
                        'name': f"{row[1]} {row[2]}"  # Combine first_name and last_name
                    })
                
                return Response(users)
        except Exception as e:
            logger.error(f"Error fetching users: {str(e)}")
            return Response({"error": f"Failed to fetch users: {str(e)}"}, status=500)
