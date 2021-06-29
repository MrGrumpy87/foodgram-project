from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientViewSet, FavoriteViewSet,
                       SubscriptionViewSet, PurchaseViewSet)

router = DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('favorites', FavoriteViewSet, basename='favorites')
router.register('subscriptions', SubscriptionViewSet, basename='subscriptions')
router.register('purchases', PurchaseViewSet, basename='purchases')

urlpatterns = [
    path('v1/', include(router.urls)),
]
