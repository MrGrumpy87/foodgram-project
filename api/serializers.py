from rest_framework import serializers

from foodgram.models import Favorite, Ingredient, Purchase, Subscription


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'dimension')
        model = Ingredient


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('recipe',)
        model = Favorite


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Subscription


class PurchaseSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('recipe',)
        model = Purchase
