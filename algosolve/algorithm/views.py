from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Category, Algorithm


POSTS_PER_PAGE = 10


def index(request):
    return HttpResponse('Hello World!')


class BaseView:
    paginate = POSTS_PER_PAGE


class CategoryListView(BaseView, ListView):
    model = Category
    template_name = 'algorithm/categories.html'

    def get_queryset(self):
        qs = self.model.objects.filter(is_published=True)
        return qs
