from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_the_pytest(self):
        ...

    def test_search_is_ok(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')
        