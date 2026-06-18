from .models import VendorApplication, VendorProfile
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def approve_application(application, admin_user):
    if VendorProfile.objects.filter(user=application.user).exists():
        raise ValueError("Vendor profile already exists.")

    VendorProfile.objects.create(
        user=application.user,
        business_name=application.business_name,
        business_description=application.business_description,
        logo=application.logo,
        support_email=application.support_email,
        support_phone=application.support_phone,
        business_address=application.business_address,
        store_slug=f"vendor-{application.user.id}"
    )

    application.status = "Approved"
    application.reviewed_by = admin_user
    application.reviewed_at = timezone.now()

    application.save()


def reject_application(application, admin_user, remarks):
    application.status = "Rejected"
    application.reviewed_by = admin_user
    application.reviewed_at = timezone.now()
    application.remarks = remarks

    application.save()


def send_vendor_email(application, subject, message):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[
                application.user.email,
                application.support_email
            ]
        )
    except Exception as e:
        logger.exception(
            f"{e}\n\nFailed to send email for application {application.id}"
        )
