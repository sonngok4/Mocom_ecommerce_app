from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm

from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserProfileForm, UserChangeAddressesForm


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


class AddressView(TemplateView):
    template_name = "user_address.html"
    form_class = UserChangeAddressesForm
    success_url = reverse_lazy("account")

    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordView(TemplateView):
    template_name = "password_change_form.html"


class PrivacySettingsView(TemplateView):
    template_name = "user_privacy_settings.html"
