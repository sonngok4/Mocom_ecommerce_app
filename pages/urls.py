from django.urls import include, path
from .views import (
    HomePageView,
    BlogPageView,
    AboutPageView,
    ProductPageView,
    ProductDetailView,
    CategoryDetailPageView,
    CategoryPageView,
    CartPageView,
    OrderPageView,
    search_results,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("blog/",BlogPageView.as_view(), name="blog"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("products/", ProductPageView.as_view(), name="products"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("categories/", CategoryPageView.as_view(), name="category"),
    path(
        "categories/<int:pk>/", CategoryDetailPageView.as_view(), name="category_detail"
    ),
    path("", include("cart.urls")),
    path("cart/", CartPageView.as_view(), name="cart"),
    path("", include("orders.urls")),
    path("order/", OrderPageView.as_view(), name="order_history"),
    path("search/", search_results, name="search_results"),
]
