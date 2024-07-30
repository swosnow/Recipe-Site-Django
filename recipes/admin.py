from django.contrib import admin


from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'id', 'titile', 'created_at', 'is_published', 'author',
    list_display_links = 'title', 'created_at',
    search_fields = 'id', 'title', 'description',
    list_filter = 'category', 'author', 'is_published',
    list_per_page = 10

    prepopulated_fields = {
        "slug": ('title',)
    }

