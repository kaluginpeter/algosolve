from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


class UserRouter(DefaultRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_lookup_regex(self, viewset, lookup_prefix=''):
        lookup_field = getattr(viewset, 'lookup_field', 'pk')
        if lookup_field == 'pk':
            lookup_field = 'username'
        base_regex = super().get_lookup_regex(viewset, lookup_prefix)
        return base_regex.replace('pk', lookup_field)


router = UserRouter()
router.register(r'profile', views.UserViewSet, basename='profile')
router.register(
    'algorithms/categories',
    views.CategoryAlgorithmViewSet,
    basename='algorithm_categories'
)
router.register(r'algorithms', views.AlogirthmViewSet, 'algorithms')
router.register(
    r'algorithms/(?P<algorithm_slug>[-\w]+)/comments',
    views.CommentAlgorithmViewSet,
    basename='algorithm_comments'
)

router.register(
    'data_structures/categories',
    views.CategoryDataStructureViewSet,
    basename='data_structure_categories'
)
router.register(
    r'data_structures',
    views.DataStructureViewSet,
    basename='data_structures'
)
router.register(
    r'data_structures/(?P<data_structure_slug>[-\w]+)/comments',
    views.CommentDataStructureViewSet,
    basename='data_structures_comments'
)

urlpatterns = [
    path('v1/', include(router.urls))
]
