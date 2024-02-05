from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.hashers import make_password

from algorithm.models import User, Category, Algorithm
from structure.models import CategoryDateStructure, DataStructure
from . import serializers as api_serialisers
from .permissions import CutsomBasePermission


class UserViewSet(ModelViewSet):
    """
    This endpoint return information about users.
    Available queries:
    GET (without username) - return list of all existing users.
    GET (with username in path) - return detail information about current user.
    Also you can perform all CRUD methods,
    like POST, PUT, PATCH, DELETE
    """
    queryset = User.objects.all()
    serializer_class = api_serialisers.FullUserSerializer
    lookup_field = 'username'
    throttle_scope = 'for_data_user_profiles'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('username', 'first_name', 'email', 'last_name')
    ordering_fields = ('username', 'first_name', 'email', 'last_name')
    search_fields = ('$username', '$first_name', '$email', '$last_name')
    ordering = ('created_at',)

    def get_serializer_class(self):
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

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if 'password' in request.data:
            password = make_password(request.data.get('password'))
            user.password = password
        self.perform_update(serializer)
        return Response(serializer.data)

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
    queryset = Category.objects.all()
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


class AlogirthmViewSet(ReadOnlyModelViewSet):
    """
    This endpoint return data about algorithms.
    Available queries:
    GET (without slug in path) - return list of all algorithms.
    GET (with slug in path) - return detail about alogrithm.
    Also you can't user any of CRUD actions here.
    """
    queryset = Algorithm.objects.all()
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
        return self.get_algorithm_by_slug().comments.all()

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
    queryset = CategoryDateStructure.objects.all()
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


class DataStructureViewSet(ReadOnlyModelViewSet):
    """
    This endpoint return data about data structures.
    Available queries:
    GET (without slug in path) - return list of all data structures.
    GET (with slug in path) - return detail about data structure.
    Also you can't user any of CRUD actions here.
    """
    queryset = DataStructure.objects.all()
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
        return self.get_data_structure_by_slug().comments.all()

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
