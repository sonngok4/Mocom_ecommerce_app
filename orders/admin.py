from django.contrib import admin

# Register your models here.

from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user","total_price", "created_at")


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product_name", "quantity", "price")
    def product_name(self, obj):
        return obj.product.name


admin.site.register(OrderItem, OrderItemAdmin)
