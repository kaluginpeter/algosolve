from http import HTTPStatus
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (
    CategoryDateStructure, DataStructure, User,
    ImageDataStructure, UrlDataStructure, CommentDataStructure,
    TaskDataStructure
)
from .forms import CommentForm


POSTS_PER_PAGE = 10



class BaseView:
    paginate = POSTS_PER_PAGE


class CategoryDataStructureListView(BaseView, ListView):
    model = CategoryDateStructure
    template_name = 'data_structure/categories.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_published=True)



class CategoryDetailView(ListView):
    model = DataStructure
    template_name = 'data_structure/category.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(category__slug=self.kwargs['category'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(CategoryDateStructure, slug=self.kwargs['category'])
        return context

class DataStructureDetailView(DetailView):
    model = DataStructure
    slug_url_kwarg = 'pk_data_structure'
    template_name = 'data_structure/data_structure_detail.html'
    _data_structure = None

    def dispatch(self, request, *args, **kwargs): 
        self._data_structure = get_object_or_404(DataStructure, slug=kwargs['pk_data_structure'])
        if (not self._data_structure.is_published
            or not self._data_structure.category.is_published
        ):
            return HttpResponse(status=HTTPStatus.NOT_FOUND)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['urls'] = UrlDataStructure.objects.filter(data_structure=self._data_structure.pk)
        context['images'] = ImageDataStructure.objects.filter(data_structure=self._data_structure.pk)
        context['tasks'] = TaskDataStructure.objects.filter(data_structure=self._data_structure.pk)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments_structure_data.select_related('data_structure', 'author')
        )
        context['data_structure'] = self.object
        return context
class CommentFormMixin:
    model = CommentDataStructure
    form_class = CommentForm
    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            CommentDataStructure.objects.select_related('author', 'data_structure'),
            pk=kwargs['pk'], data_structure__slug=kwargs['pk_data_structure'])
        if instance.author != request.user:
            return redirect('data_structure:data_structure_detail', self.kwargs['pk_category'], self.kwargs['pk_data_structure'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('data_structure:data_structure_detail',
                       kwargs={'pk_category': self.kwargs['pk_category'], 'pk_data_structure': self.kwargs['pk_data_structure']})
class CommentCreateView(LoginRequiredMixin, CreateView):
    data_structure = None
    model = CommentDataStructure
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs): 
        self.data_structure = DataStructure.objects.filter(category__slug=self.kwargs['pk_category']).get(slug=kwargs['pk_data_structure']) 
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.data_structure = self.data_structure
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('data_structure:data_structure_detail', kwargs={'pk_data_structure': self.data_structure.slug, 'pk_category': self.data_structure.category.slug})

class CommentUpdateView(LoginRequiredMixin, CommentFormMixin, UpdateView):
    template_name = 'data_structure/comment.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.object  # or however you obtain your comment object
        return context
class CommentDeleteView(LoginRequiredMixin, DeleteView, CommentFormMixin):
    model = CommentDataStructure
    template_name = 'data_structure/comment.html'
    success_url = reverse_lazy('algorithm:index')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.object  # or however you obtain your comment object
        return context
    def get_success_url(self):
        return reverse('data_structure:data_structure_detail', kwargs={'pk_category': self.kwargs['pk_category'], 'pk_data_structure': self.kwargs['pk_data_structure']}) + '#comments_an'
