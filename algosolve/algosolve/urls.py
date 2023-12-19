from django.contrib import admin, auth
from django.urls import path, include, reverse_lazy
from django.conf.urls.static import static
from django.views.generic.edit import CreateView

from . import settings

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
    path('pages/', include('pages.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'pages.views.page_not_found'

handler500 = 'pages.views.server_error'
