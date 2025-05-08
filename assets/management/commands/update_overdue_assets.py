from django.core.management.base import BaseCommand
from django.utils import timezone
from assets.models import AssetCheckout
from assets.utils import send_overdue_notifications

class Command(BaseCommand):
    help = 'Updates the status of overdue asset checkouts and sends notifications'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        
        # Update overdue checkouts
        overdue_checkouts = AssetCheckout.objects.filter(
            status='CHECKED_OUT',
            expected_return_date__lt=now,
            actual_return_date__isnull=True
        )

        count = 0
        for checkout in overdue_checkouts:
            if checkout.status != 'OVERDUE':
                checkout.status = 'OVERDUE'
                checkout.save()
                count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {count} overdue checkouts')
        )

        # Send notifications for overdue and upcoming returns
        try:
            send_overdue_notifications()
            self.stdout.write(
                self.style.SUCCESS('Successfully sent overdue and reminder notifications')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error sending notifications: {str(e)}')
            )