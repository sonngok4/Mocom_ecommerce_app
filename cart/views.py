from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from product.models import Product
from .models import Cart, CartItem


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse(
            {
                "success": True,
                "quantity": cart_item.quantity,
                "total_price": float(cart_item.total_price),
            }
        )

    return redirect("product_detail", product_id)


@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    return render(request, "cart.html", {"cart_items": cart_items})


@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = request.POST.get("quantity")
    cart_item.quantity = int(quantity)
    cart_item.save()
    data = {
        "success": True,
        "id": cart_item.pk,
        "quantity": cart_item.quantity,
        "total_price": cart_item.total_price,
        # Include any other data you want to return
    }
    return JsonResponse(data)


@login_required
def delete_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart = cart_item.cart
    cart_item.delete()

    # Update the cart total price
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.total_price for item in cart_items)
    cart.total_price = total_price
    cart.save()

    return redirect("cart")

@login_required
def delete_all_items(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()
    cart_items.delete()
    cart.total_price = 0
    cart.save()
    return redirect("cart")
