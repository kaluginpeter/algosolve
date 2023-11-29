from django.contrib import admin
from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.PagesAboutViews.as_view(), name='about'),
    path('rules/', views.PagesRulesViews.as_view(), name='rules'),
]