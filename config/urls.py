from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from config import views

handler404 = 'config.views.page_not_found' # noqa
handler500 = 'config.views.server_error' # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('api/', include('api.urls')),
    path('', include('foodgram.urls')),
    path('about-author/',
         views.about,
         name='about-author'),
    path('about-tech/',
         views.about,
         name='about-tech')
]

if settings.DEBUG:
    import debug_toolbar

    # Debug toolbar endpoints
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
