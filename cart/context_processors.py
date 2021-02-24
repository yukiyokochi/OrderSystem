from .models import Cart, CartItem
from ec.models import Location
from .views import _cart_id
from django.core.exceptions import ObjectDoesNotExist
import payjp

def counter(request):
    item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                item_count += cart_item.quantity
        except Cart.DoesNotExist:
            item_count = 0
    return dict(item_count = item_count)


def cart_detail(request, total=0, counter=0, cart_items = [], location = []):
    try:
        if "location" in request.session:
            location_index = request.session.get("location")
            location = Location.objects.get(id=location_index)
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, active=True)
        else:
            location = Location.objects.get(id=1)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
        totalandship = total + location.shippingtax

    except ObjectDoesNotExist:
        pass

    return dict(cart_items = cart_items, total = total, counter = counter, location = location)
