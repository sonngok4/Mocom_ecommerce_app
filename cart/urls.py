from django.urls import path
from . import views

urlpatterns = [
    path(
        "cart/item/<int:item_id>/update/",
        views.update_cart_item,
        name="update_cart_item",
    ),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/<int:item_id>/delete/", views.delete_cart_item, name="delete_cart_item"),
    path("cart/delete/", views.delete_all_items, name="delete_all_items")
]
