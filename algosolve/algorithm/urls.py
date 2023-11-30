from django.contrib import admin
from django.urls import path

from . import views

app_name = 'algorithm'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'profile/<slug:username>/',
        views.UserProfileListView.as_view(), name='profile'),
    path(
        'algorithms/categories/',
        views.CategoryListView.as_view(), name='categories'),
    path(
        'algorithms/categories/category_detail/<slug:categpry/',
        views.CategoryDetailView.as_view(), name='category_detail'),
    path( 
        'edit_profile/', views.UserChangeProfileView.as_view(),
        name='edit_profile'),
]