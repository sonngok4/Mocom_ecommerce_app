from django.conf import settings
from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from product.models import Product
from django.contrib.auth.decorators import login_required


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="carts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Sắp xếp mặc định khi query là giảm dần theo ngày tạo
        ordering = ["-created_at"]
        indexes = [
            # Chỉ mục index sẽ đánh theo field created_at
            models.Index(fields=["created_at"])
        ]


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )  # in cents

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.product.price
        super().save(*args, **kwargs)

    @classmethod
    def delete_item(cls, item_id, user):
        # Retrieve the cart item from the database
        cart_item = get_object_or_404(cls, id=item_id, cart__user=user)

        # Delete the cart item
        cart_item.delete()

        # Return a JSON response indicating success
        return JsonResponse({"success": True})

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


@login_required
def delete_cart_item(request, item_id):
    CartItem.delete_item(item_id, request.user)
    return redirect("cart")
