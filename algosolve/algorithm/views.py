from typing import Any
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, Algorithm, User
from .forms import ChangeUserNameForm


POSTS_PER_PAGE = 10


def index(request):
    template = 'algorithm/index.html'
    return render(request, template)


class BaseView:
    paginate = POSTS_PER_PAGE


class CategoryListView(BaseView, ListView):
    model = Category
    template_name = 'algorithm/categories.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_published=True)



class CategoryDetailView(ListView):
    model = Algorithm
    template_name = 'algorithm/category.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(category__slug=self.kwargs['category'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['category'])
        context['urls'] = get_object_or_404(Category, slug=self.kwargs['category']).urls.all()
        context['images'] = get_object_or_404(Category, slug=self.kwargs['category']).images.all()
        return context


class UserProfileListView(ListView):
    model = User
    template_name = 'algorithm/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username'])
        return context


class UserChangeProfileView(LoginRequiredMixin, UpdateView): 
    model = User
    form_class = ChangeUserNameForm
    template_name = 'algorithm/user.html'

    def get_object(self, queryset=False):
        return self.request.user

    def get_success_url(self): 
        return reverse('blog:profile', kwargs={
            'username': self.get_object().username})
