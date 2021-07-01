from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('favorites/', views.favorites, name='favorites'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('purchases/', views.purchases, name='purchases'),
    path('purchases/download/',
         views.purchases_file,
         name='purchases_download'),
    path('recipes/add/', views.recipe_create, name='create'),
    path('recipes/<int:recipe_id>/', views.detail, name='recipe'),
    path('recipes/<int:recipe_id>/edit/', views.recipe_edit, name='edit'),
    path('recipes/<int:recipe_id>/delete/',
         views.recipe_delete,
         name='delete'),
    path('profile/<str:username>/', views.profile, name='profile'),
]
