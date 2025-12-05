from django.core.mail import send_mail
from django.conf import settings

def send_invitation(invitation):
    subject = "You have been invited to join our platform"

    message = (
        f"Hello!\n\n"
        f"You have been invited to join our platform.\n"
        f"Click the link below to accept your invitation:\n\n"
        f"{settings.SENDING_DOMAIN}/invite/{invitation.id}\n\n"
        f"This invitation will expire on {invitation.expires_at}.\n\n"
        f"Kind regards,\n"
        f"The Team"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [invitation.email],
        fail_silently=False,
    )