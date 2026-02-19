from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from products.models import Product


def cart_detail(request):
    raw_cart = request.session.get("cart", {})
    items = []
    total = 0

    for product_id, quantity in raw_cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        total += subtotal
        items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    bought = request.GET.get("bought") == "1"
    return render(
        request,
        "cart/cart_detail.html",
        {"items": items, "total": total, "bought": bought},
    )


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get("cart", {})
    key = str(product.id)
    cart[key] = cart.get(key, 0) + 1
    request.session["cart"] = cart
    request.session.modified = True
    return redirect(request.POST.get("next") or "cart_detail")


@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    key = str(product_id)
    if key in cart:
        del cart[key]
        request.session["cart"] = cart
        request.session.modified = True
    return redirect("cart_detail")


@require_POST
def buy_cart(request):
    request.session["cart"] = {}
    request.session.modified = True
    return redirect("/cart/?bought=1")
