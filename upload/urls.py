from django.urls import path
from upload import views

urlpatterns = [
    path("upload-images/", views.PhotoAPIView.as_view()),
    path("upload-images/<str:photo_id>/", views.PhotoAPIView.as_view()),
]
