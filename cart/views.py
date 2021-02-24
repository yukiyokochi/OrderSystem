from django.shortcuts import render, redirect, get_object_or_404
from ec.models import Menu, Location
from .models import Cart, CartItem, Form
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views import generic
from .forms  import OrderForm
from django.views.generic import View
import payjp
from django.http import HttpResponse
from django.conf import settings

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, pk):
    product = Menu.objects.get(id=pk)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
                cart_id =  _cart_id(request)
            )
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart
            )
        cart_item.save()
    return redirect('cart:cart_detail')

def cart_detail(request, total=0, counter=0, cart_items = [], location = []):
    try:
        if "location" in request.session:
            location_index = request.session.get("location")
            location = Location.objects.get(id=location_index)
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    return render(request, 'cart/cart.html', dict(cart_items = cart_items, total = total, counter = counter, location = location))

def cart_remove(request, pk):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Menu, id=pk)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')

def contact_form(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            if request.POST.getlist('payway') == ['1']:
                form.save()
                return redirect('cart:thanks')
            elif request.POST.getlist('payway') == ['2']:
                form.save()
                return redirect('cart:payjp')
    else:
        form = OrderForm()
    return render(request, 'cart/form.html', {'form': form})

class PayView(View):
    def get(self, request):
        return render(
            request, "cart/payjp.html", {"public_key":"pk_test_c8c8b495f0cc632e85fcf253"}
        )

    def post(self, request):
        amount = request.POST.get("amount")
        payjp_token = request.POST.get("payjp-token")
        customer = payjp.Customer.create(email="example@pay.jp", card=payjp_token)
        charge = payjp.Charge.create(
            amount=amount,
            currency="jpy",
            customer=customer.id,
            description="Django example charge",
        )
        context = {
            "amount":amount,
            "customer":customer,
            "charge":charge,
            'order_list':Form.objects.all().order_by('-created_at')[:1],
        }
        return render(request, 'cart/payjp.html', context)


def thanks_page(request):
    context = {
        'order_list': Form.objects.all().order_by('-created_at')[:1],
    }
    return render(request, 'cart/thanks.html', context)
