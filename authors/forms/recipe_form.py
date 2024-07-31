from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from collections import defaultdict
from django.core.exceptions import ValidationError

class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)
        

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        


    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', 'preparation_time_unit', 'servings', 'servings_unit', 'preparation_steps', 'cover'

        wigets = {
            'cover': forms.FileInput(
                attrs={
                    'class':'span-2'
                }
            ),
            'servings_units': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            )
        }
    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if len(title) < 5:
            self._my_errors['title'].append('Must have at least 5 chars')
        
        if title == description:
            self._my_errors['title'].append('Cannot be equal to description')
            self._my_errors['description'].append('Cannot be equal to title')
        
        
        if self._my_errors:
            raise ValidationError(self._my_errors)
        return super_clean