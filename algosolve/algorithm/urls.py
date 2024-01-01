from django.contrib import admin
from django.urls import path

from . import views

app_name = 'algorithm'

urlpatterns = [
    path('', views.index, name='index'),
    path('roadmap/', views.RoadMapStaticView.as_view(), name='roadmap'),
    path('theory/', views.TheoryAlgorithms.as_view(), name='theory'),
    path(
        'algorithm_in_structure/', views.AlgorithmInStructure.as_view(),
        name='algorithm-in-structure'),
    path(
        'optimize_algorithms/', views.OptimizeAlgoritm.as_view(),
        name='optimize-algorithms'),
    path(
        'profile/<slug:username>/',
        views.UserProfileListView.as_view(), name='profile'),
    path(
        'algorithms/categories/',
        views.CategoryListView.as_view(), name='categories'),
    path(
        'algorithms/category_detail/<slug:category>/',
        views.CategoryDetailView.as_view(), name='category_detail'),
    path(
        'algorithms/<slug:pk_category>/<slug:pk_algorithm>/',
        views.AlgorithmDetailView.as_view(), name='algorithm_detail'),
    path( 
        'edit_profile/', views.UserChangeProfileView.as_view(),
        name='edit_profile'),
    path(
        'algorithms/<slug:pk_category>/<slug:pk_algorithm>/edit_comment/<int:pk>/',
        views.CommentUpdateView.as_view(),
        name='edit_comment'),

    path(
        'algorithms/<slug:pk_category>/<slug:pk_algorithm>/delete_comment/<int:pk>/',
        views.CommentDeleteView.as_view(),
        name='delete_comment'),
    path(
        'algorithms/<slug:pk_category>/<slug:pk_algorithm>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment'),
]