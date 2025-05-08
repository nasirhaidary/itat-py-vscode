from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

def send_checkout_notification(checkout):
    """Send email notification when an asset is checked out"""
    if not settings.ASSET_NOTIFICATION_SETTINGS['ENABLE_NOTIFICATIONS']:
        return

    subject = f'Asset Checkout: {checkout.asset.asset_id}'
    context = {
        'user': checkout.checked_out_by,
        'asset': checkout.asset,
        'checkout': checkout,
    }
    
    # Email to user
    user_message = render_to_string('assets/email/checkout_user.html', context)
    user_email = [(
        subject,
        user_message,
        settings.DEFAULT_FROM_EMAIL,
        [checkout.checked_out_by.email],
    )]

    # Email to admin
    if settings.ASSET_NOTIFICATION_SETTINGS['ADMIN_EMAIL']:
        admin_message = render_to_string('assets/email/checkout_admin.html', context)
        admin_email = [(
            f'[ADMIN] {subject}',
            admin_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ASSET_NOTIFICATION_SETTINGS['ADMIN_EMAIL']],
        )]
        emails = user_email + admin_email
    else:
        emails = user_email

    try:
        send_mass_mail(tuple(emails), fail_silently=False)
        logger.info(f'Sent checkout notification for asset {checkout.asset.asset_id}')
    except Exception as e:
        logger.error(f'Failed to send checkout notification: {str(e)}')

def send_checkin_notification(checkout):
    """Send email notification when an asset is checked in"""
    if not settings.ASSET_NOTIFICATION_SETTINGS['ENABLE_NOTIFICATIONS']:
        return

    subject = f'Asset Check-in: {checkout.asset.asset_id}'
    context = {
        'user': checkout.checked_out_by,
        'asset': checkout.asset,
        'checkout': checkout,
    }
    
    # Email to admin
    if settings.ASSET_NOTIFICATION_SETTINGS['ADMIN_EMAIL']:
        message = render_to_string('assets/email/checkin_admin.html', context)
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ASSET_NOTIFICATION_SETTINGS['ADMIN_EMAIL']],
                fail_silently=False
            )
            logger.info(f'Sent check-in notification for asset {checkout.asset.asset_id}')
        except Exception as e:
            logger.error(f'Failed to send check-in notification: {str(e)}')

def send_overdue_notifications():
    """Send notifications for overdue assets and upcoming returns"""
    if not settings.ASSET_NOTIFICATION_SETTINGS['ENABLE_NOTIFICATIONS']:
        return

    from .models import AssetCheckout  # Import here to avoid circular imports
    
    now = timezone.now()
    reminder_days = settings.ASSET_NOTIFICATION_SETTINGS['OVERDUE_REMINDER_DAYS']
    
    # Find assets due soon
    due_soon = AssetCheckout.objects.filter(
        status='CHECKED_OUT',
        expected_return_date__range=(
            now,
            now + timedelta(days=reminder_days)
        )
    )
    
    # Find overdue assets
    overdue = AssetCheckout.objects.filter(
        status='CHECKED_OUT',
        expected_return_date__lt=now
    )
    
    emails = []
    
    # Process due soon notifications
    for checkout in due_soon:
        context = {
            'user': checkout.checked_out_by,
            'asset': checkout.asset,
            'checkout': checkout,
            'days_remaining': (checkout.expected_return_date - now).days
        }
        message = render_to_string('assets/email/due_soon_reminder.html', context)
        emails.append((
            f'Asset Return Reminder: {checkout.asset.asset_id}',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [checkout.checked_out_by.email]
        ))
    
    # Process overdue notifications
    for checkout in overdue:
        context = {
            'user': checkout.checked_out_by,
            'asset': checkout.asset,
            'checkout': checkout,
            'days_overdue': (now - checkout.expected_return_date).days
        }
        # Email to user
        user_message = render_to_string('assets/email/overdue_reminder.html', context)
        emails.append((
            f'OVERDUE Asset: {checkout.asset.asset_id}',
            user_message,
            settings.DEFAULT_FROM_EMAIL,
            [checkout.checked_out_by.email]
        ))
        
        # Email to admin
        if settings.ASSET_NOTIFICATION_SETTINGS['ADMIN_EMAIL']:
            admin_message = render_to_string('assets/email/overdue_admin.html', context)
            emails.append((
                f'[ADMIN] OVERDUE Asset: {checkout.asset.asset_id}',
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ASSET_NOTIFICATION_SETTINGS['ADMIN_EMAIL']]
            ))
    
    if emails:
        try:
            send_mass_mail(tuple(emails), fail_silently=False)
            logger.info(f'Sent {len(emails)} overdue/reminder notifications')
        except Exception as e:
            logger.error(f'Failed to send overdue/reminder notifications: {str(e)}')