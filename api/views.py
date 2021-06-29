from rest_framework import filters, mixins, viewsets

from api.mixins import MixinView
from api.serializers import (IngredientSerializer, FavoriteSerializer,
                             SubscriptionSerializer, PurchaseSerializer)
from foodgram.models import Ingredient, Favorite, Subscription, Purchase


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^title',)


class FavoriteViewSet(MixinView):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    field_name = 'recipe_id'


class SubscriptionViewSet(MixinView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    field_name = 'author_id'


class PurchaseViewSet(MixinView):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
    field_name = 'recipe_id'
