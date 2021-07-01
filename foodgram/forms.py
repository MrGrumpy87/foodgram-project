from django import forms
from django.db import transaction
from django.forms import CheckboxSelectMultiple
from django.shortcuts import get_object_or_404

from foodgram.models import Ingredient, Recipe, Tag
from foodgram.utils import get_ingredient


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                          widget=CheckboxSelectMultiple())

    class Meta:
        model = Recipe
        fields = (
            'name',
            'image',
            'description',
            'cooking_time',
            'ingredients',
            'tags'
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form__input'}),
            'cooking_time': forms.TextInput(
                attrs={'class': 'form__input'}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form__textarea', 'rows': '8'}
            ),
            'image': forms.ClearableFileInput(
                attrs={'class': 'form__file-button'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ingredients'].required = False
        self.fields['tags'].required = False

    def clean(self):
        cleaned_data = super().clean()
        tags = self.fields['tags'].choices.queryset.all()
        tags_on = []
        for tag in tags:
            if self.data.get(tag.slug) == 'on':
                tags_on.append(tag)
        if not tags_on:
            self._errors['name'] = self.error_class(
                ['Необходимо выбрать время приема пищи'])
        cleaned_data['tags'] = tags_on

        ingredients_obj = []
        amount_list = []
        for key, value in self.data.items():
            if key.startswith('nameIngredient_'):
                ingredient = get_object_or_404(Ingredient, title=value)
                ingredients_obj.append(ingredient)
            elif key.startswith('valueIngredient_'):
                if int(value) < 0:
                    self._errors['ingredients'] = self.error_class(
                        ['Количество ингридиентов должно быть больше 0'])
                amount_list.append(int(value))
        if not len(ingredients_obj):
            self._errors['ingredients'] = self.error_class(
                ['Не выбраны ингридиенты. Выберите хотя бы один'])
        cleaned_data['nameIngredients'] = ingredients_obj
        cleaned_data['valueIngredient'] = amount_list
        return cleaned_data

    def save(self, commit=True):
        with transaction.atomic():
            recipe = super().save(commit=False)
            if commit:
                recipe.save()
                recipe_ingredients_count = recipe.recipe_ingredients.count()
                recipe.tags.set(self.cleaned_data.get('tags'))
                if recipe_ingredients_count > 0:
                    recipe.recipe_ingredients.all().delete()
                get_ingredient(self, recipe)
            return recipe
