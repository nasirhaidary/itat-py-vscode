from django.core.management.base import BaseCommand
from django.utils import timezone
from assets.models import AssetCheckout

class Command(BaseCommand):
    help = 'Updates the status of overdue asset checkouts'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        overdue_checkouts = AssetCheckout.objects.filter(
            status='CHECKED_OUT',
            expected_return_date__lt=now,
            actual_return_date__isnull=True
        )

        count = 0
        for checkout in overdue_checkouts:
            checkout.status = 'OVERDUE'
            checkout.save()
            count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {count} overdue checkouts')
        )