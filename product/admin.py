from django.contrib import admin
from .models import Category, Product, ProductImage, ProductComment, WishlistItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "icon_url"]


admin.site.register(Category, CategoryAdmin)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "category_id",
        "name",
        "unit",
        "price",
        "discount",
        "amount",
        "is_public",
        "thumbnail",
        "description"
    ]

    inlines = [
        ProductImageInline,
    ]


admin.site.register(ProductImage)


@admin.action(description="Mark selected products as public")
def make_public(modeladmin, request, queryset):
    queryset.update(is_public=True)


@admin.action(description="Mark selected products as private")
def make_private(modeladmin, request, queryset):
    queryset.update(is_public=False)


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ["id", "rating", "comment", "product_id", "created_at"]
    actions = [make_public, make_private]


# Registering the wishlist item to the admin site
admin.site.register(WishlistItem)
