from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef

from foodgram.models import Purchase, Favorite, RecipeIngredient, Tag, Recipe


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
    tags_on = request.GET.getlist('tags', [])
    if tags_on:
        obj_list = obj_list.filter(tags__slug__in=tags_on).distinct()
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


def get_ingredient(form, recipe):
    ingredients = form.cleaned_data.get('nameIngredients')
    amounts = form.cleaned_data.get('valueIngredient')
    recipe_ingredients_obj = []
    for ingredient, amount in zip(ingredients, amounts):
        recipe_ingredients_obj.append(RecipeIngredient(
            recipe=recipe,
            ingredient=ingredient,
            amount=amount
        ))
    RecipeIngredient.objects.bulk_create(recipe_ingredients_obj)
