from django.urls import path
from .views import SignUpView, UserProfileView, AddressView, PrivacySettingsView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("account/profile/", UserProfileView.as_view(), name="account"),
    path("account/address/", AddressView.as_view(), name="address"),
    path("privacy_settings/", PrivacySettingsView.as_view(), name="privacy_settings"),
]
