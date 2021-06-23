from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets, status
from rest_framework.response import Response

from api.serializers import IngredientSerializer, FavoriteSerializer, SubscriptionSerializer, PurchaseSerializer
from foodgram.models import Ingredient, Favorite, Recipe, Subscription, Purchase

User = get_user_model()


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
	queryset = Ingredient.objects.all()
	serializer_class = IngredientSerializer
	filter_backends = (filters.SearchFilter,)
	search_fields = ('^title',)


class MixinView(
	mixins.ListModelMixin,
	mixins.CreateModelMixin,
	mixins.DestroyModelMixin,
	LoginRequiredMixin,
	viewsets.GenericViewSet):
	field_name = None

	def get_queryset(self):
		queryset = self.queryset.filter(user=self.request.user)
		return queryset

	def get_object(self):
		obj = None
		queryset = self.get_queryset()
		if self.field_name == 'recipe_id':
			obj = get_object_or_404(queryset, recipe_id=self.kwargs['pk'])
		elif self.field_name == 'author_id':
			obj = get_object_or_404(queryset, author_id=self.kwargs['pk'])
		return obj

	def perform_create(self, serializer):
		if self.field_name == 'recipe_id':
			obj = get_object_or_404(Recipe, id=self.request.data['id'])
			serializer.save(recipe=obj, user=self.request.user)
		elif self.field_name == 'author_id':
			obj = get_object_or_404(User, id=self.request.data['id'])
			serializer.save(author=obj, user=self.request.user)

	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		self.perform_destroy(instance)
		return Response({"success": True}, status=status.HTTP_200_OK)


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
