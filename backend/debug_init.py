import os
import django

print("Setting DJANGO_SETTINGS_MODULE...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
print("Calling django.setup()...")
try:
    django.setup()
    print("Django setup complete.")
except Exception as e:
    print(f"Error during django.setup(): {e}")

from django.db import connection
print("Checking database connection...")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("Database connection primary check okay.")
except Exception as e:
    print(f"Error during database check: {e}")
