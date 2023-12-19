from django.urls import path

from . import views

app_name = 'data_structure'

urlpatterns = [

    path(
        'categories/',
        views.CategoryDataStructureListView.as_view(), name='categories'),
    path(
        'category_structure_detail/<slug:category>/',
        views.CategoryDetailView.as_view(), name='category_detail'),
    path(
        '<slug:pk_category>/<slug:pk_data_structure>/',
        views.DataStructureDetailView.as_view(), name='data_structure_detail'),
    path(
        '<slug:pk_category>/<slug:pk_data_structure>/edit_comment/<int:pk>/',
        views.CommentUpdateView.as_view(),
        name='edit_comment'),

    path(
        '<slug:pk_category>/<slug:pk_data_structure>/delete_comment/<int:pk>/',
        views.CommentDeleteView.as_view(),
        name='delete_comment'),
    path(
        '<slug:pk_category>/<slug:pk_data_structure>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment'),
]