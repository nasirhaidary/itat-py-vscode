import os
import sys
import django
from datetime import datetime

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'it_asset_tracker.settings')
django.setup()

from django.core.management import call_command
from django.utils import timezone

def main():
    # Log the start of the check
    print(f"[{timezone.now()}] Starting overdue assets check...")
    
    try:
        # Run the management command
        call_command('update_overdue_assets')
        print(f"[{timezone.now()}] Overdue assets check completed successfully")
    except Exception as e:
        print(f"[{timezone.now()}] Error during overdue assets check: {str(e)}")

if __name__ == '__main__':
    main()