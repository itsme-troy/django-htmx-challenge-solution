from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts_app.forms import InviteUserForm
from accounts_app.models import UserInvitation


class InviteUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # This would be the view where the invited user can join.
        # Here we have to check if the provided token points to an invitation which is valid and not expired.
        # ...

        """
        HTMX GET request loads the modal UI.
        If it's not HTMX, then fallback to rendering profile page.
        """
        form = InviteUserForm()

        # HTMX request to show the modal
        if request.headers.get("Hx-Request") == "true":
            return render(
                request,
                "accounts_app/fragments/invite_modal.html",
                {"invite_user_form": form},
            )

        # Normal (non-HTMX) fallback (rarely used)
        return render(
            request,
            "accounts_app/profile.html",
            {"invite_user_form": form},
        )

    def post(self, request, *args, **kwargs):
        """
            Handles invite submission.
            Creates the DB record and returns either:
            - success modal fragment
            - or form re-rendered with errors
        """

        form = InviteUserForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data["email"]

            # Remove old invites for same email
            UserInvitation.objects.filter(email=email).delete()

            # # We could further improve this here to first check if an invitation for this email already exists and is not expired
            # UserInvitation.objects.filter(email=form.cleaned_data["email"]).delete()

            invitation = UserInvitation(email=email, invited_by=request.user)

            # invitation = UserInvitation(email=form.cleaned_data["email"], invited_by=request.user)
            invitation.save()

            # OUT OF SCOPE: sending real email → we print instead
            invitation.send_invitation_email()


              # Success response for HTMX: update the modal body
            if request.headers.get("Hx-Request") == "true":
                return render(
                    request,
                    "accounts_app/fragments/invite_success_fragment.html",
                    {"email": email},
                )

            # Fallback (non-HTMX)
            return render(
                request,
                "accounts_app/profile.html",
                {
                    "invite_user_form": InviteUserForm(),
                    "invited": True,
                },
            )
        # If form invalid — return error fragment inside modal
        if request.headers.get("Hx-Request") == "true":
            return render(
                request,
                "accounts_app/fragments/invite_form_fragment.html",
                {"invite_user_form": form},
            )

        # Non-HTMX fallback
        return render(
            request,
            "accounts_app/profile.html",
            {"invite_user_form": form},
        )