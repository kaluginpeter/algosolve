from django.contrib import admin, auth
from django.conf import settings
from django.urls import path, include, reverse_lazy
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from graphene_django.views import GraphQLView

from . import settings
from api.yasg import urlpatterns as doc_urls

urlpatterns = [
    path('', include('algorithm.urls')),
    path('data_structures/', include('structure.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', CreateView.as_view(
        template_name='registration/registration_form.html',
        form_class=auth.forms.UserCreationForm,
        success_url=reverse_lazy('algorithm:index')),
        name='registration'),
    path('pages/', include('pages.urls')),
    path('api/', include('api.urls')),
    # Djoser создаст набор необходимых эндпоинтов.
    # базовые, для управления пользователями в Django:
    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('auth/', include('djoser.urls.jwt')),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True)))
]

urlpatterns += doc_urls

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )



handler404 = 'pages.views.page_not_found'

handler500 = 'pages.views.server_error'
