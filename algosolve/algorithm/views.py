from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, Algorithm, User
from .forms import ChangeUserNameForm


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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['category_obj'] = self.model.objects.filter(is_published=True)
        return context


class CategoryDetailView(ListView):
    model = Category


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
