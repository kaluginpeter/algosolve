from http import HTTPStatus
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, Algorithm, User, ImageAlgorithm, UrlAlgorithm, Comment, TaskAlgorithm, UrlTaskAlgorithm
from .forms import ChangeUserNameForm, CommentForm


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

class AlgorithmDetailView(DetailView):
    model = Algorithm
    slug_url_kwarg = 'pk_algorithm'
    template_name = 'algorithm/algorithm_detail.html'
    algorithm = None

    def dispatch(self, request, *args, **kwargs): 
        self.algorithm = get_object_or_404(Algorithm, slug=kwargs['pk_algorithm'])
        if (not self.algorithm.is_published
            or not self.algorithm.category.is_published
        ):
            return HttpResponse(status=HTTPStatus.NOT_FOUND)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['urls'] = UrlAlgorithm.objects.filter(algorithm=self.algorithm.pk)
        context['images'] = ImageAlgorithm.objects.filter(algorithm=self.algorithm.pk)
        context['tasks'] = TaskAlgorithm.objects.filter(algorithm=self.algorithm.pk)
        context['online_tasks'] = UrlTaskAlgorithm.objects.filter(algorithm=self.algorithm.pk)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('algorithm', 'author')
        )
        return context
class CommentFormMixin:
    model = Comment
    form_class = CommentForm
    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Comment.objects.select_related('author', 'algorithm'),
            pk=kwargs['pk'], algorithm__slug=kwargs['pk_algorithm'])
        if instance.author != request.user:
            return redirect('algorithm:algorithm_detail', self.kwargs['pk_category'], self.kwargs['pk_algoritm'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('algorithm:algorithm_detail',
                       kwargs={'pk_category': self.kwargs['pk_category'], 'pk_algorithm': self.kwargs['pk_algorithm']})
class CommentCreateView(LoginRequiredMixin, CreateView):
    _algorithm = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs): 
        self._algorithm = Algorithm.objects.filter(category__slug=self.kwargs['pk_category']).get(slug=kwargs['pk_algorithm']) 
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.algorithm = self._algorithm
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('algorithm:algorithm_detail', kwargs={'pk_algorithm': self._algorithm.slug, 'pk_category': self._algorithm.category.slug})

class CommentUpdateView(LoginRequiredMixin, CommentFormMixin, UpdateView):
    template_name = 'algorithm/comment.html'

class CommentDeleteView(LoginRequiredMixin, DeleteView, CommentFormMixin):
    model = Comment
    template_name = 'algorithm/comment.html'
    success_url = reverse_lazy('algorithm:index')
    def get_success_url(self):
        return reverse('algorithm:algorithm_detail', kwargs={'pk_category': self.kwargs['pk_category'], 'pk_algorithm': self.kwargs['pk_algorithm']}) + '#comments_an'

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
        return reverse('algorithm:profile', kwargs={
            'username': self.get_object().username})

class RoadMapStaticView(TemplateView):
    template_name = 'algorithm/roadmap.html'