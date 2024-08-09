from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views

class TestRecipeViewFuncton(TestCase):

    def test_recipe_home(self):
        view = resolve('/')
        self.assertIs(view.func, views.home)

    def test_recipe_category(self):
        view = resolve(reverse('recipes:category', args=(1,)))
        self.assertIs(view.func, views.category)

    def test_recipe_recipes_function(self):
        view = resolve(reverse('recipes:recipe', args=(1,)))
        self.assertIs(view.func, views.recipe)

    def test_recipe_search(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)
    
    def test_recipe_like_dislike(self):
        view = resolve(reverse('recipes:like_dislike'))
        self.assertIs(view.func, views.like_dislike)

    #check status code is ok

    def test_recipe_home_client_status_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')