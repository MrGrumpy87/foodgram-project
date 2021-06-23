from django import forms

from foodgram.models import Recipe, Ingredient, Tag


class RecipeForm(forms.ModelForm):
	class Meta:
		model = Recipe
		fields = (
			'name',
			'image',
			'description',
			'cooking_time',
			'ingredients',
			'tag'
		)
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form__input'}),
			'ingredients': forms.TextInput(attrs={'class': 'form__input', 'id': 'nameIngredient'}),
			'cooking_time': forms.TextInput(attrs={'class': 'form__input'}),
			'description': forms.Textarea(attrs={'class': 'form__textarea', 'rows': '8'}),
			'image': forms.ClearableFileInput(attrs={'class': 'form__file-button'}, )
		}

	def __init__(self, *args, **kwargs):
		super(RecipeForm, self).__init__(*args, **kwargs)
		self.fields['ingredients'].required = False
		self.fields['tag'].required = False

	def clean(self):
		cleaned_data = super(RecipeForm, self).clean()

		tags = ('breakfast', 'lunch', 'dinner')
		tags_on = []
		for i in tags:
			if self.data.get(i) == 'on':
				tags_on.append(i)
		if not tags_on:
			self._errors['name'] = self.error_class(
				['Необходимо выбрать время приема пищи'])
		cleaned_data['tags'] = Tag.objects.filter(slug__in=tags_on)

		ingredients_obj = []
		amount_list = []
		for key, value in self.data.items():
			if key.startswith('nameIngredient_'):
				ingredient = Ingredient.objects.get(title=value)
				ingredients_obj.append(ingredient)
			elif key.startswith('valueIngredient_'):
				if int(value) < 0:
					self._errors['ingredients'] = self.error_class(
						['Количество ингридиентов должно быть больше 0'])
				amount_list.append(int(value))
		if not len(ingredients_obj):
			self._errors['ingredients'] = self.error_class(['Не выбраны ингридиенты. Выберите хотя бы один'])
		cleaned_data['nameIngredients'] = ingredients_obj
		cleaned_data['valueIngredient'] = amount_list

		return cleaned_data
