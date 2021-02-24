from django.test import TestCase

# Create your tests here.
from django.shortcuts import resolve_url

class ViewTest(TestCase):
    def test_homepage_view_and_content(self):
        response = self.client.get(resolve_url('homepage:top'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Portfolio of Yokochi Yuki")
