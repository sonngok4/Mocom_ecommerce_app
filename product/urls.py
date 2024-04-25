from django.urls import path
from .views import (
    CategoryAPIView,
    CategoryDetailAPIView,
    ProductViewAPI,
    ProductDetailAPIView,
    ProductImageAPIView,
    ProductImageDetailAPIView,
    ProductCommentAPIView,
    ProductCommentDetailAPIView,
)

urlpatterns = [
    path("category/", CategoryAPIView.as_view()),
    path("category/<slug:id_slug>/", CategoryDetailAPIView.as_view()),
    path("product/<slug:product_id_slug>/images/", ProductImageAPIView.as_view()),
    path(
        "product/<slug:product_id_slug>/images/<slug:id_slug>/",
        ProductImageDetailAPIView.as_view(),
    ),
    path(
        "product/<slug:product_id_slug>/comments/",
        ProductCommentAPIView.as_view(),
    ),
    path(
        "product/<slug:product_id_slug>/comments/<slug:id_slug>/",
        ProductCommentDetailAPIView.as_view(),
    ),
    path("product/", ProductViewAPI.as_view()),
    path("product/<slug:id_slug>/", ProductDetailAPIView.as_view()),
]
