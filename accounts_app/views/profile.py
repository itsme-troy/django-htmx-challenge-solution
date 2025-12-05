from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts_app.forms import EditUserForm, InviteUserForm


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "accounts_app/profile.html", {
            "form": EditUserForm(instance=request.user),
            "invite_user_form": InviteUserForm() 
        })
    
    def post(self, request, *args, **kwargs):         # activates when the user submits the Edit Profile form
        # Create form instance from submitted form data
        form = EditUserForm(request.POST, instance=request.user)
        invite_user_form = InviteUserForm()

        if form.is_valid():
            form.save() # updates the user.

            # reload the user and re-render clean form
            # The re-render shows correct values on screen
            form = EditUserForm(instance=request.user)

            return render(request, "accounts_app/profile.html", {
                "form": form, 
                "invite_user_form": invite_user_form, 
                "updated": True,  # optional flag for UI feedback
            })
        #  If invalid → return with errors
        return render( request, "accounts_app/profile.html", {
            "form": form,
            "invite_user_form": invite_user_form
            }
        )
