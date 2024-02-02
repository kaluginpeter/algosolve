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
            author = get_object_or_404(
                User, username=self.kwargs.get('username')
            )
            if self.request.user != author:
                return api_serialisers.UserSerializer
            else:
                return api_serialisers.FullUserSerializer
        if self.action == 'list':
            return api_serialisers.UserSerializer
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
    serializer_class = api_serialisers.CommentAlgorithmSerializer
    lookup_field = 'id'
    permission_classes = (CutsomBasePermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('created_at',)
    ordering_fields = ('created_at', 'text')
    search_fields = ('$created_at', '$text', '$author__username')
    ordering = ('created_at',)

    def get_algorithm_by_slug(self):
        return get_object_or_404(Algorithm, slug=self.kwargs.get('post_slug'))

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
