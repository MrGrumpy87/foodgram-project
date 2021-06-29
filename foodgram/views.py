import io

import pdfkit
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from config.settings import RECIPE_IN_PAGE
from foodgram.forms import RecipeForm
from foodgram.models import Recipe, Favorite, Subscription, Purchase
from foodgram.utils import paginator_on_page

User = get_user_model()


def index(request):
    page_title = 'Рецепты'
    paginator_by = RECIPE_IN_PAGE
    template_page = 'foodgram/index.html'
    recipes = Recipe.objects.all()
    context = paginator_on_page(request, recipes, paginator_by, page_title)
    return render(request, template_page, context)


@login_required()
def favorites(request):
    page_title = 'Избранное'
    paginator_by = RECIPE_IN_PAGE
    template_page = 'foodgram/favorite_list.html'
    favorites_recipes = Recipe.objects.filter(favorites__user=request.user)
    
    context = paginator_on_page(request, favorites_recipes,
                                paginator_by, page_title)
    return render(request, template_page, context)


@login_required()
def subscriptions(request):
    page_title = 'Мои подписки'
    paginator_by = 3
    template_page = 'foodgram/myFollow_list.html'
    subscriptions_authors = Subscription.objects.filter(user=request.user)
    context = paginator_on_page(request, subscriptions_authors,
                                paginator_by, page_title)
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
    ingredients = recipes_list.order_by(
        'ingredients__title'
    ).values(
        'ingredients__title',
        'ingredients__dimension'
    ).annotate(total_quantity=Sum('recipe_ingredients__amount'))
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
    paginator_by = RECIPE_IN_PAGE
    template_page = 'foodgram/profile_list.html'
    author = get_object_or_404(User, username=username)
    author_recipes = author.recipes.all()
    context = paginator_on_page(request, author_recipes,
                                paginator_by, page_title)
    if not request.user.is_authenticated:
        return render(request, template_page, context)
    is_subscriptions = Subscription.objects.filter(
        user_id=request.user,
        author_id=author
    ).exists()
    context.update({
        'is_subscriptions': is_subscriptions
    })
    return render(request, template_page, context)


def detail(request, recipe_id):
    page_title = 'Детали рецепта'
    template_page = 'foodgram/detail_recipe.html'
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {
        'page_title': page_title,
        'recipe': recipe
    }
    if not request.user.is_authenticated:
        return render(request, template_page, context)
    is_favorites = Favorite.objects.filter(
        user_id=request.user,
        recipe_id=recipe_id
    ).exists()
    is_subscriptions = Subscription.objects.filter(
        user_id=request.user,
        author_id=recipe.author
    ).exists()
    is_purchases = Purchase.objects.filter(
        user_id=request.user,
        recipe_id=recipe_id
    ).exists()
    recipe_atr = {
        'is_favorites': is_favorites,
        'is_purchases': is_purchases,
        'is_subscriptions': is_subscriptions
    }
    context.update({
        'recipe_atr': recipe_atr
    })
    return render(request, template_page, context)


@login_required
def recipe_create(request):
    page_title = 'Создание рецепта'
    template_page = 'foodgram/recipe_form.html'
    form = RecipeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.instance.author = request.user
        recipe = form.save()
        return redirect('recipe', recipe_id=recipe.id)
    context = {
        'form': form,
        'page_title': page_title,
    }
    return render(request, template_page, context)


@login_required
def recipe_edit(request, recipe_id):
    page_title = 'Редактирование рецепта'
    template_page = 'foodgram/recipe_form.html'
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe', recipe_id=recipe.id)
    form = RecipeForm(request.POST or None,
                      request.FILES or None,
                      instance=recipe)
    if form.is_valid():
        recipe = form.save()
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
