from django.http import HttpRequest
from django.test import TestCase

from django.urls import resolve
from django.test import TestCase
from .views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!doctype html>'))
        self.assertIn('<title>Hotel Scrapping</title>', html)
        self.assertTrue(html.endswith('</html>'))