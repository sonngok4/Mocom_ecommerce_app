from cart.models import CartItem
from product.models import Category, Product


def product_cart_and_categories(request):
    return {
        "products": Product.objects.all(),
        "cart_items": CartItem.objects.all(),
        "categories": Category.objects.all(),
    }
