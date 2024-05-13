from django.urls import path
from . import views

urlpatterns = [
    path("create-order/", views.create_order, name="create_order"),
    path("order-history/", views.order_history, name="order_history"),
    path("checkout/<int:order_id>", views.order_checkout, name="order_checkout"),
    path("checkout-failed", views.checkout_failed, name="checkout_failed"),
    path("place-order/<int:order_id>", views.place_order, name="place_order"),
    path("products/<int:product_id>/buy-now/", views.buy_now, name="buy_now"),
]
