from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_the_pytest(self):
        ...

    def test_search_is_ok(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')
        
    def test_recipe_home_url_is_correct(self):
        home = reverse('recipes:home')
        self.assertEqual(home, '/') 
