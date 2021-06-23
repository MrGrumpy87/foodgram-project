import io

import pdfkit
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Exists, OuterRef, Sum
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from foodgram.forms import RecipeForm
from foodgram.models import Recipe, RecipeIngredient, Favorite, Subscription, Purchase, Tag

User = get_user_model()


def recipe_annotate(recipe_list, login_user):
	recipe = recipe_list.annotate(
		is_purchase=Exists(
			Purchase.objects.filter(
				user_id=login_user,
				recipe_id=OuterRef('pk'),
			),
		),
		is_favorite=Exists(
			Favorite.objects.filter(
				user_id=login_user,
				recipe_id=OuterRef('pk'),
			),
		),
	)
	return recipe


def paginator_on_page(request, obj_list, paginator_by, page_title):
	tags_on = request.GET.getlist("tags", [])
	if tags_on:
		obj_list = obj_list.filter(tag__slug__in=tags_on).distinct()
	page_number = request.GET.get('page')
	if request.user.is_authenticated and obj_list.model is Recipe:
		obj_list = recipe_annotate(obj_list, request.user)
	paginator = Paginator(obj_list, paginator_by)
	page = paginator.get_page(page_number)
	get_copy = request.GET.copy()
	parameters = get_copy.pop('page', True) and get_copy.urlencode()
	context = {
		'page_title': page_title,
		'tags': Tag.objects.all(),
		'page_obj': page,
		'paginator': paginator,
		'parameters': parameters
	}
	return context


def index(request):
	page_title = 'Рецепты'
	paginator_by = 6
	template_page = 'foodgram/index_Auth.html'
	recipes = Recipe.objects.all()
	context = paginator_on_page(request, recipes, paginator_by, page_title)
	if not request.user.is_authenticated:
		template_page = 'foodgram/index_NotAuth.html'
	return render(request, template_page, context)


@login_required()
def favorites(request):
	page_title = 'Избранное'
	paginator_by = 6
	template_page = 'foodgram/favorite_list.html'
	favorites_recipes = Recipe.objects.filter(favorites__user=request.user)
	context = paginator_on_page(request, favorites_recipes, paginator_by, page_title)
	return render(request, template_page, context)


@login_required()
def subscriptions(request):
	page_title = 'Мои подписки'
	paginator_by = 3
	template_page = 'foodgram/myFollow_list.html'
	subscriptions_authors = Subscription.objects.filter(user=request.user)
	context = paginator_on_page(request, subscriptions_authors, paginator_by, page_title)
	return render(request, template_page, context)


@login_required()
def purchases(request):
	page_title = 'Список покупок'
	template_page = 'foodgram/purchase_list.html'
	purchases_list = Purchase.objects.filter(user=request.user)
	context = {
		'page_title': page_title,
		'page_obj': purchases_list
	}
	return render(request, template_page, context)


@login_required()
def purchases_file(request):
	recipes_list = Recipe.objects.filter(purchases__user=request.user)
	ingredients = recipes_list.order_by("ingredients__title").\
		values("ingredients__title", "ingredients__dimension").\
		annotate(total_quantity=Sum('recipeIngredients__amount'))
	rendered = render_to_string(
		'foodgram/purchases_download.html',
		{
			'recipes_list': recipes_list,
			'ingredients': ingredients
		},
	)
	pdf_file = pdfkit.from_string(rendered, False)
	buffer = io.BytesIO(pdf_file)
	return FileResponse(buffer, as_attachment=True, filename='purchases.pdf')


def profile(request, username):
	page_title = f'Рецепты {username}'
	paginator_by = 6
	template_page = 'foodgram/profile_list.html'
	author = get_object_or_404(User, username=username)
	author_recipes = author.recipes.all()
	context = paginator_on_page(request, author_recipes, paginator_by, page_title)
	if not request.user.is_authenticated:
		return render(request, template_page, context)
	is_subscriptions = Subscription.objects.filter(user_id=request.user, author_id=author).exists()
	context.update({
		'is_subscriptions': is_subscriptions
	})
	return render(request, template_page, context)


def detail(request, recipe_id):
	page_title = 'Детали рецепта'
	template_page = 'foodgram/detail_recipe_Auth.html'
	recipe = get_object_or_404(Recipe, id=recipe_id)
	context = {
		'page_title': page_title,
		'recipe': recipe
	}
	if not request.user.is_authenticated:
		template_page = 'foodgram/detail_recipe_NotAuth.html'
		return render(request, template_page, context)
	is_favorites = Favorite.objects.filter(user_id=request.user, recipe_id=recipe_id).exists()
	is_subscriptions = Subscription.objects.filter(user_id=request.user, author_id=recipe.author).exists()
	is_purchases = Purchase.objects.filter(user_id=request.user, recipe_id=recipe_id).exists()
	recipe_atr = {
		'is_favorites': is_favorites,
		'is_purchases': is_purchases,
		'is_subscriptions': is_subscriptions
	}
	context.update({
		'recipe_atr': recipe_atr
	})
	return render(request, template_page, context)


def get_ingredient(form, recipe):
	ingredients_obj = form.cleaned_data.get('nameIngredients')
	amount_list = form.cleaned_data.get('valueIngredient')
	recipe_ingredients_obj = []
	for i in range(len(ingredients_obj)):
		recipe_ingredients_obj.append(RecipeIngredient(
			recipe=recipe,
			ingredient=ingredients_obj[i],
			amount=amount_list[i]
		))
	RecipeIngredient.objects.bulk_create(recipe_ingredients_obj)


@login_required
def recipe_create(request):
	page_title = 'Создание рецепта'
	template_page = 'foodgram/recipe_add_form.html'
	tags = Tag.objects.all()
	form = RecipeForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		with transaction.atomic():
			recipe = form.save(commit=False)
			recipe.author = request.user
			recipe.save()
			recipe.tag.set(form.cleaned_data.get('tags'))
			get_ingredient(form, recipe)
		return redirect('recipe', recipe_id=recipe.id)
	context = {
		'form': form,
		'page_title': page_title,
		'tags': tags
	}
	return render(request, template_page, context)


@login_required
def recipe_edit(request, recipe_id):
	page_title = 'Редактирование рецепта'
	template_page = 'foodgram/recipe_change_form.html'
	recipe = get_object_or_404(Recipe, id=recipe_id)
	if request.user != recipe.author:
		return redirect('recipe', recipe_id=recipe.id)
	form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)
	if form.is_valid():
		with transaction.atomic():
			recipe.tag.set(form.cleaned_data.get('tags'))
			recipe.save()
			recipe.recipeIngredients.all().delete()
			get_ingredient(form, recipe)
		return redirect('recipe', recipe_id=recipe.id)
	context = {
		'form': form,
		'page_title': page_title,
		'recipe': recipe}
	return render(request, template_page, context)


@login_required
def recipe_delete(request, recipe_id):
	recipe = get_object_or_404(Recipe, author=request.user, id=recipe_id)
	recipe.delete()
	return redirect('index')
