import uuid

from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings

from .user import User


def get_expiration_datetime():
    return timezone.now() + timezone.timedelta(days=settings.USER_INVITE_EXPIRATION_DAYS)


class UserInvitation(models.Model):
    # Must be a UUID for security reasons. UUID can not be guessed.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # email being invited
    email = models.EmailField(max_length=255, unique=True)
    
    # who invited the user
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    # expiration logic 
    expires_at = models.DateTimeField(default=get_expiration_datetime)

    # disable email sending since its out of scope 
    def send_invitation_email(self):
        # Instead of sending, we simply print the placeholder message.
        print(f"[INVITATION GENERATED] Email: {self.email}, Token: {self.id}")

        # send_mail(
        #     "You have been invited to join our platform",
        #     f"Click here to join: { settings.SENDING_DOMAIN }/invite/{self.id}",
        #     "Kind regards, The Team",
        #     [self.email],
        # )