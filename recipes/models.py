from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import os
from django.conf import settings
from PIL import Image

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)


    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=64)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d', blank=True, default='')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, default=None,)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse('recipes:recipe', args={self.id,})
    
    @staticmethod
    def resizeImage(image, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(img_full_path)
        original_width, original_height = image_pillow.size

        if original_width < new_width:
            image_pillow.close()
            return
        new_height = round((new_width * original_height) / original_width)
        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(img_full_path, optmize=True, quality=60)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resizeImage(self.cover, 840)
            except FileNotFoundError:
                ...
        return saved