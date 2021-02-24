from django.test import TestCase

# Create your tests here.
from django.shortcuts import resolve_url
from .models import Cart, CartItem, Payment, Form
from ec.models import Menu, Category, Location, ChoiceLocation
from django.utils import timezone
from .views import cart_detail
from .forms  import OrderForm
import payjp

class ModelTest(TestCase):
    def test_cart_model(self):
        obj = Cart(cart_id=0)
        self.assertEqual(0, obj.__str__())

    def test_cartitem_model(self):
        category_obj = Category.objects.create(name = 'ドリンク')
        menu_obj = Menu.objects.create(
            name = '生ビール',
            category = category_obj,
            price = 800
        )
        cart_obj = Cart.objects.create(
            cart_id = 0,
            date_added = timezone.now()
        )
        obj = CartItem(
            product = menu_obj,
            cart = cart_obj,
            quantity = 3,
            active = True
        )
        self.assertEqual(2400, obj.sub_total())
        self.assertEqual('生ビール', obj.__str__())

    def test_payment_model(self):
        obj = Payment(name='クレジットカード')
        self.assertEqual('クレジットカード', obj.__str__())

    def test_form_model(self):
        payment_obj = Payment.objects.create(name='クレジットカード')
        obj = Form(
            name = '山田太郎',
            address = '東京都墨田区',
            tel = '09012345678',
            email = 'example@gmail.com',
            payway = payment_obj,
            text = '特になし',
            created_at = timezone.now(),
            location = 'エリアA',
            order_content = '生ビール',
            totalprice = 800,
            myself = True
        )
        self.assertEqual('山田太郎', obj.__str__())

class ViewTest(TestCase):
    def test_cart_detail_view(self):
        response = self.client.get(resolve_url('cart:cart_detail'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.context['total'])
        self.assertEqual([], response.context['cart_items'])
        self.assertEqual(0, response.context['counter'])
        self.assertEqual([], response.context['location'])
        self.assertContains(response, "カートは空です。")

    def test_contact_form_view(self):
        location_create = Location.objects.create(name = 'エリアB',shippingtax=100,shippingtime=20,mustorderprice=1000)
        choice_location_obj = ChoiceLocation(location=location_create)
        response = self.client.get(resolve_url('cart:form'))
        self.assertEqual(200, response.status_code)
        self.assertIn('お名前', str(response.context['form']))
        self.assertIn('ご住所', str(response.context['form']))
        self.assertIn('注文内容', str(response.context['form']))

    def test_pay_view(self):
        location_create = Location.objects.create(name = 'エリアB',shippingtax=100,shippingtime=20,mustorderprice=1000)
        choice_location_obj = ChoiceLocation(location=location_create)
        response = self.client.get(resolve_url('cart:payjp'))
        self.assertEqual(200, response.status_code)
        self.assertEqual('pk_test_c8c8b495f0cc632e85fcf253', response.context['public_key'])
        self.assertContains(response, "お支払い")


    def test_thanks_page_view(self):
        location_create = Location.objects.create(name = 'エリアB',shippingtax=100,shippingtime=20,mustorderprice=1000)
        choice_location_obj = ChoiceLocation(location=location_create)
        response = self.client.get(resolve_url('cart:thanks'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "注文ありがとうございました。")
