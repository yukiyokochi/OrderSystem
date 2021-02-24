from django.test import TestCase

# Create your tests here.
from django.shortcuts import resolve_url
from .models import Menu, Category, Location, ChoiceLocation
from .forms import LocationRegisterForm

class ModelTest(TestCase):
    def test_menu_model(self):
        obj = Menu(name='生ビール')
        self.assertEqual('生ビール', obj.__str__())

    def test_category_model(self):
        obj = Category(name='ドリンク')
        self.assertEqual('ドリンク', obj.__str__())

    def test_location_model(self):
        location_obj = Location(name='エリアA')
        self.assertEqual('エリアA', location_obj.__str__())
        location_create = Location.objects.create(name = 'エリアB',shippingtax=100,shippingtime=20,mustorderprice=1000)
        choice_location_obj = ChoiceLocation(location=location_create)
        self.assertEqual('エリアB', str(choice_location_obj.__str__()))

class ViewTest(TestCase):
    def test_ec_location_register_view(self):
        response = self.client.get(resolve_url('ec:location_register'))
        self.assertEqual(200, response.status_code)
        self.assertIn('住所', str(response.context['form']))

    def test_ec_menu_list_view(self):
        response = self.client.get(resolve_url('ec:menu_list'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.context['category_list'].count())

        Category.objects.create(name = 'ドリンク')

        response = self.client.get(resolve_url('ec:menu_list'))
        self.assertEqual(1, response.context['category_list'].count())

    def test_ec_menu_detail_view(self):
        response = self.client.get(resolve_url('ec:menu_detail',pk=1))
        self.assertEqual(404, response.status_code)

        category_obj1 = Category.objects.create(name = 'ドリンク')

        Menu.objects.create(
            name = '生ビール',
            category = category_obj1,
            price = 800
        )
        response = self.client.get(resolve_url('ec:menu_detail',pk=1))
        self.assertEqual(200, response.status_code)
        response = self.client.get(resolve_url('ec:menu_detail',pk=2))
        self.assertEqual(404, response.status_code)

        category_obj2 = Category.objects.create(name = 'メイン')

        Menu.objects.create(
            name = '肉',
            category = category_obj2,
            price = 1000
        )
        response = self.client.get(resolve_url('ec:menu_detail',pk=2))
        self.assertEqual(200, response.status_code)
