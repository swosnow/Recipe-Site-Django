from django.shortcuts import render, get_list_or_404, redirect
from django.urls import reverse
from recipes.models import Recipe, Like
from django.http.response import Http404
from django.db.models import Q
from django.core.paginator import Paginator
from .utils.pagination import make_pagination
from django.contrib import messages
import os



PER_PAGE = os.environ.get('PER_PAGE', 6)

def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=category_id,
        is_published=True,
    ).order_by('-id')
    )
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    
    return render(request, 'recipes/pages/home.html', context={

        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'{recipes[0].category.name} - Category | '
    })


def recipe(request, id):
    recipe = Recipe.objects.filter(pk=id, is_published=True,).order_by('-id').first()
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe':recipe,
        'is_detail_page': True,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        return Http404()

    recipes = Recipe.objects.filter(
        Q(
            
            Q(title__icontains=search_term) | 
            Q(description__icontains=search_term)
        
        ), is_published=True).order_by('-id')
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)


    return render(request, 'recipes/pages/search.html',
                  {'page_title': f'Search for "{search_term}" |', 
                   'search_term': search_term,
                   'recipes': page_obj,
                   'pagination_range':pagination_range,
                   'additional_url_query': f'&q={search_term}'
    })

def like_dislike(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            post_id = request.POST.get('post_id')
            post_obj = Recipe.objects.get(id=post_id)

            if user in post_obj.likes.all():
                post_obj.likes.remove(user)
            else:
                post_obj.likes.add(user)
            like, created = Like.objects.get_or_create(user=user, post_id=post_id)

            if not created:
                if like.value == 'Like':
                    like.value = 'Unlike'
                else:
                    like.value = 'Like'
            like.save()

            return redirect(reverse('recipes:home'))
           
    
    else:
        messages.success(request, ("You Must be logged in!"))
        return redirect('recipes:home')