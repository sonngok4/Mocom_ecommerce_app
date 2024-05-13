from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import CartItem
from .models import Order, OrderItem
from product.models import Product


@login_required
def create_order(request):
    if request.method == "POST":
        # Get the selected product IDs from the request
        selected_product_ids = request.POST.getlist("selected_products")

        if not selected_product_ids:
            # If no products are selected, display an error message
            messages.error(request, "Please select at least one product to checkout.")
            return redirect("cart")
        cart_items = CartItem.objects.filter(product_id__in=selected_product_ids)
        print(selected_product_ids)
        print(cart_items)

        # Calculate the total price
        total_price = sum(cart_item.total_price for cart_item in cart_items)
        print("Total Price:", total_price)

        # Create a new order
        order = Order.objects.create(user=request.user, total_price=total_price)

        # Create order items
        for cart_item in cart_items:
            product = cart_item.product
            quantity = cart_item.quantity
            price = product.price
            total_price = price * quantity  # Calculate total price
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
                total_price=total_price,  # Set total price
            )
        return redirect("order_checkout", order_id=order.pk)

    # Render the order creation template
    products = Product.objects.all()
    return render(request, "create_order.html", {"products": products})


@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    print(product.name)

    if request.method == "POST":
        quantity = int(request.POST.get("purchase-quantity", 1))
        total_price = quantity * product.price

        # Create a new order
        order = Order.objects.create(user=request.user, total_price=total_price)

        # Create an order item
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price,
            total_price=product.price * quantity,
        )

        # Render the order_checkout.html template
        return render(
            request,
            "order_checkout.html",
            {
                "order": order,
                "order_items": [order_item],
                "user": request.user,
            },
        )

    return redirect("product_detail", pk=product_id)


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
    return render(request, "order_history.html", {"orders": orders})


@login_required
def order_checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    context = {
        "order": order,
        "order_items": order_items,
    }
    return render(request, "order_checkout.html", context)

@login_required
def checkout_failed(request):
    
    return render(request, "checkout_failed.html")

@login_required
def place_order(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id, user=request.user)
        order_items = OrderItem.objects.filter(order=order)
        context = {
            "order": order,
            "order_items": order_items,
        }
        return render(request, "order_successful.html", context)
    return redirect("cart")
