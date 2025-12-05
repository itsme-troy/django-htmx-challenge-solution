import uuid

from django.db import models
from django.core.mail import send_mail # Django’s built-in function for sending emails.
from django.utils import timezone # used for time calculations.
from django.conf import settings

from .user import User # custom User model.

from accounts_app.services.invitation_service import send_invitation

import logging
logger = logging.getLogger(__name__)

# Returns the expiration date for the invitation.
def get_expiration_datetime():
    return timezone.now() + timezone.timedelta(days=settings.USER_INVITE_EXPIRATION_DAYS)


class UserInvitation(models.Model):
    # UUID is more secure and can not be guessed compared to integer
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Stores the email address of the invitee.
    email = models.EmailField(
        max_length=255, 
        unique=True # ensures we cannot invite the same email twice
    ) 
    
    # Links the invitation to the User who sent it.
    invited_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE # If the inviter’s account is deleted, the invitation is also deleted.
    )

    # Automatically stores the date/time the invitation was created.
    created_at = models.DateTimeField(auto_now_add=True)
    # expiration logic 
    expires_at = models.DateTimeField(default=get_expiration_datetime)

    # send an invite email.
    def send_invitation_email(self):
        # Delegate email sending to the service layer.
        send_invitation(self)

       # we print the email content to the console.
        logger.info(f"Invitation sent to {self.email} with token {self.id}")
