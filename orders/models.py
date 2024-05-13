from django.db import models
from django.conf import settings
from product.models import Product  # Assuming you have a 'products' app


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    products = models.ManyToManyField(Product, through="OrderItem")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Sắp xếp mặc định khi query là giảm dần theo ngày tạo
        ordering = ["-created_at"]
        indexes = [
            # Chỉ mục index sẽ đánh theo field created_at
            models.Index(fields=["created_at"])
        ]

    def __str__(self):
        return f"Order {self.id} by {self.user.username} (Total: {self.total_price})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Price: {self.price})"
