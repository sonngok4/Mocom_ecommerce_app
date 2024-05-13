from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_filter = ("user",)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("name_product", "unit_price", "quantity", "total_price")

    def unit_price(self, obj):
        # Retrieve the unit price from the related Product model
        return obj.product.price
    def name_product(self, obj):
        # Retrieve the product name from the related Product model
        return obj.product.name
    name_product.short_description = "Product Name"
    unit_price.short_description = (
        "Unit Price"  # Set the column header text for unit price
    )


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
