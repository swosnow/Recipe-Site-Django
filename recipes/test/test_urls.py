from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_the_pytest(self):
        ...

    def test_search_is_ok(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')
    
    def test_category_is_ok(self):
        url = reverse('recipes:category', args=(1,))
        self.assertEqual(url, '/recipes/category/1/')

    def test_detail_is_ok(self):
        url = reverse('recipes:recipe', args=(1,))
        self.assertEqual(url, '/recipes/1/')

    def test_like_dislike_is_ok(self):
        url = reverse('recipes:like_dislike')
        self.assertEqual(url, '/recipes/like_dislike/')