from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.hashers import make_password

from algorithm.models import User, Algorithm, Comment
from structure import models as structure_models
from algorithm import models as algorithm_models
from structure.models import DataStructure, CommentDataStructure
from . import serializers as api_serialisers
from .permissions import CutsomBasePermission, ProfilePermission


class UserViewSet(ModelViewSet):
    """
    This endpoint return information about users.
    Available queries:
    GET (without username) - return list of all existing users.
    GET (with username in path) - return detail information about current user.
    Also you can perform all CRUD methods,
    like POST, PUT, PATCH, DELETE
    """
    permission_classes = (ProfilePermission,)
    serializer_class = api_serialisers.FullUserSerializer
    lookup_field = 'username'
    throttle_scope = 'for_data_user_profiles'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('username', 'first_name', 'email', 'last_name')
    ordering_fields = ('username', 'first_name', 'email', 'last_name')
    search_fields = ('$username', '$first_name', '$email', '$last_name')
    ordering = ('created_at',)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return User.objects.none()
        return User.objects.all()

    def get_serializer_class(self):
        if getattr(self, 'swagger_fake_view', False):
            return api_serialisers.FullUserSerializer
        if self.action == 'retrieve':
            author = User.objects.get(username=self.kwargs.get('username'))
            if self.request.user != author:
                return api_serialisers.CustomUserSerializer
            else:
                return api_serialisers.FullUserSerializer
        if self.action == 'list':
            return api_serialisers.CustomUserSerializer
        return api_serialisers.FullUserSerializer

    def perform_update(self, serializer):
        author = get_object_or_404(User, username=self.kwargs.get('username'))

        if self.request.user != author:
            raise PermissionDenied("You can't change not own data")
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        if self.request.user != author:
            raise PermissionDenied("You can't change not own data")
        return super(UserViewSet, self).perform_destroy(instance)


class CategoryAlgorithmViewSet(ReadOnlyModelViewSet):
    """
    This endpoints give all information about categories of algorithms.
    Available queries:
    GET (without slug of category) - return list of all categories algorithms.
    GET (with slug in path) - return detail about current category.
    And in this endpoint you can't perform any of CRUD actions.
    """
    serializer_class = api_serialisers.CategoryAlgorithmSerializer
    lookup_field = 'slug'
    permission_classes = (CutsomBasePermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('created_at', 'slug', 'title')
    ordering_fields = ('created_at', 'slug', 'title')
    search_fields = ('$created_at', '$slug', '$title')
    ordering = ('created_at',)

    def get_serializer_class(self):
        if self.action == 'list':
            return api_serialisers.CategoryAlgorithmSerializer
        return api_serialisers.FullCategoryAlgorithmSerializer

    def get_queryset(self):
        new_queryset = algorithm_models.Category.objects.all() \
            .prefetch_related('algorithms')
        return new_queryset


class AlogirthmViewSet(ReadOnlyModelViewSet):
    """
    This endpoint return data about algorithms.
    Available queries:
    GET (without slug in path) - return list of all algorithms.
    GET (with slug in path) - return detail about alogrithm.
    Also you can't user any of CRUD actions here.
    """
    serializer_class = api_serialisers.AlgorithmSerializer
    lookup_field = 'slug'
    permission_classes = (CutsomBasePermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('created_at', 'category__slug', 'title')
    ordering_fields = ('created_at', 'text', 'category_slug')
    search_fields = ('$created_at', '$text', '$category_slug', '$slug')
    ordering = ('created_at',)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return api_serialisers.FullAlgorithmSerializer
        return api_serialisers.AlgorithmSerializer

    def get_queryset(self):
        new_queryset = Algorithm.objects.all().select_related('category') \
            .prefetch_related(
                'photo_algorithm', 'task_to_algorithm',
                'url_to_theory_algorithm',
                'url_to_online_tasks', 'comments', 'comments__author'
            )
        return new_queryset


class CommentAlgorithmViewSet(ModelViewSet):
    """
    This end point return datas about comments in algorithm.
    Available queries:
    GET (without id_comment in path) - return all comments
    under current algorithm. You can use all of CRUD action,
    just describe id current comment in path (exclude POST method).
    """
    serializer_class = api_serialisers.CommentAlgorithmSerializer
    lookup_field = 'id'
    permission_classes = (CutsomBasePermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('created_at',)
    ordering_fields = ('created_at', 'text')
    search_fields = ('$created_at', '$text', '$author__username')
    ordering = ('created_at',)

    def get_algorithm_by_slug(self):
        return get_object_or_404(
            Algorithm, slug=self.kwargs.get('algorithm_slug')
        )

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.all()
        return Comment.objects.filter(
            algorithm__slug=self.kwargs.get('algorithm_slug')
            ).select_related('algorithm', 'author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            algorithm=self.get_algorithm_by_slug()
        )

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied("You can't change not own data")
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied("You can't change not own data")
        return super(CommentAlgorithmViewSet, self).perform_destroy(instance)


class CategoryDataStructureViewSet(ReadOnlyModelViewSet):
    """
    This endpoints give all information about categories of data structures.
    Available queries:
    GET (without slug of category) - return list
    of all categories data structures.
    GET (with slug in path) - return detail about current category.
    And in this endpoint you can't perform any of CRUD actions.
    """
    serializer_class = api_serialisers.CategoryDataStructureSerializer
    lookup_field = 'slug'
    permission_classes = (CutsomBasePermission,)
    permission_classes = (CutsomBasePermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('created_at', 'slug', 'title')
    ordering_fields = ('created_at', 'slug', 'title')
    search_fields = ('$created_at', '$slug', '$title')
    ordering = ('created_at',)

    def get_serializer_class(self):
        if self.action == 'list':
            return api_serialisers.CategoryDataStructureSerializer
        return api_serialisers.FullCategoryDataStructureSerializer

    def get_queryset(self):
        new_queryset = structure_models.CategoryDateStructure.objects.all() \
            .prefetch_related('data_structures')
        return new_queryset


class DataStructureViewSet(ReadOnlyModelViewSet):
    """
    This endpoint return data about data structures.
    Available queries:
    GET (without slug in path) - return list of all data structures.
    GET (with slug in path) - return detail about data structure.
    Also you can't user any of CRUD actions here.
    """
    serializer_class = api_serialisers.DataStructureSerializer
    lookup_field = 'slug'
    permission_classes = (CutsomBasePermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('created_at', 'category__slug', 'title')
    ordering_fields = ('created_at', 'text', 'category_slug')
    search_fields = ('$created_at', '$text', '$category_slug', '$slug')
    ordering = ('created_at',)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return api_serialisers.FullDataStructureSerializer
        return api_serialisers.DataStructureSerializer

    def get_queryset(self):
        new_queryset = structure_models.DataStructure.objects.all() \
            .select_related('category').prefetch_related(
            'photo_data_structure', 'task_to_data_structure',
            'url_to_theory_data_structure', 'comments', 'comments__author'
        )
        return new_queryset


class CommentDataStructureViewSet(ModelViewSet):
    """
    This end point return datas about comments in data structure.
    Available queries:
    GET (without id_comment in path) - return all comments
    under current data structure. You can use all of CRUD action,
    just describe id current comment in path (exclude POST method).
    """
    serializer_class = api_serialisers.CommentDataStructureSerializer
    lookup_field = 'id'
    permission_classes = (CutsomBasePermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('created_at',)
    ordering_fields = ('created_at', 'text')
    search_fields = ('$created_at', '$text', '$author__username')
    ordering = ('created_at',)

    def get_data_structure_by_slug(self):
        return get_object_or_404(
            DataStructure, slug=self.kwargs.get('data_structure_slug')
        )

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CommentDataStructure.objects.all()
        return structure_models.CommentDataStructure.objects.filter(
            data_structure__slug=self.kwargs.get('data_structure_slug')
            ).select_related('author', 'data_structure')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            data_structure=self.get_data_structure_by_slug()
        )

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied("You can't change not own data")
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied("You can't change not own data")
        return super(
            CommentDataStructureViewSet, self
        ).perform_destroy(instance)
