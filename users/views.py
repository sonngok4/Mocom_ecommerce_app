from django.db.models.base import Model as Model
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm

from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserProfileForm, UserChangeAddressForm

from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect, render


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = "user_profile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy(
        "account"
    )  # Redirect to account page after form submission

    def get_object(self, queryset=None):
        return self.request.user  # Get the current user as the object for the form


class AddressView(LoginRequiredMixin, UpdateView):
    template_name = "user_address.html"
    form_class = UserChangeAddressForm
    success_url = reverse_lazy("account")

    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordView(TemplateView):
    template_name = "password_change_form.html"


class PrivacySettingsView(TemplateView):
    template_name = "user_privacy_settings.html"

    def delete_account(request):
        if request.method == "POST":
            # Perform account deletion logic here
            user = request.user
            user.delete()
            logout(request)
            messages.success(request, "Your account has been deleted.")
            return redirect("home")
        return render(request, "user_privacy_settings.html")
