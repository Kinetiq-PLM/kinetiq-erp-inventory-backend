import traceback
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Diagnose database connectivity and table access'

    def handle(self, *args, **options):
        try:
            # Set search path
            with connection.cursor() as cursor:
                cursor.execute("SET search_path TO public, inventory, admin, human_resources")
                
                # Database connection check
                self.stdout.write(self.style.SUCCESS('Database Connection: Successful'))
                
                # Schemas check
                cursor.execute("SELECT schema_name FROM information_schema.schemata")
                schemas = cursor.fetchall()
                self.stdout.write(self.style.SUCCESS('\nAvailable Schemas:'))
                for schema in schemas:
                    self.stdout.write(schema[0])
                
                # Table existence check
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'inventory' 
                        AND table_name = 'inventory_cyclic_counts'
                    )
                """)
                table_exists = cursor.fetchone()[0]
                self.stdout.write(self.style.SUCCESS(f'\nTable inventory.inventory_cyclic_counts exists: {table_exists}'))
                
                # Column check
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_schema = 'inventory' 
                    AND table_name = 'inventory_cyclic_counts'
                """)
                columns = cursor.fetchall()
                self.stdout.write(self.style.SUCCESS('\nColumns in inventory_cyclic_counts:'))
                for column in columns:
                    self.stdout.write(column[0])
                
                # Sample data check
                cursor.execute("SELECT * FROM inventory.inventory_cyclic_counts LIMIT 5")
                rows = cursor.fetchall()
                self.stdout.write(self.style.SUCCESS(f'\nNumber of rows retrieved: {len(rows)}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
            self.stdout.write(self.style.ERROR(traceback.format_exc()))