from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from foodgram import views

handler404 = 'foodgram.views.page_not_found' # noqa
handler500 = 'foodgram.views.server_error' # noqa

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
