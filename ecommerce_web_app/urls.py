"""
URL configuration for ecommerce_web_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),  # homepage and about page are in pages app
    path("", include("product.urls")),  # products app contains all product related urls
    path("users/", include("users.urls")),  # new
    path("users/", include("django.contrib.auth.urls")),  # new
    # path("", include("cart.urls")),  # cart app contains all cart related urls
    # path("", include("oders.urls")),  # oders app contains all oders related urls
    path("", include("upload.urls")),
    path("api/v1/", include("upload.urls")),
    path("api/v1/", include("djoser.urls")),
    path("api/v1/", include("djoser.urls.jwt")),
]
