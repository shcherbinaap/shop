from django.urls import path, include
from django.contrib import admin
from mainapp import views as mainapp_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainapp_views.main, name = 'main'),
    path('products/', include('mainapp.urls', namespace = 'products')),
    path('auth/', include('authapp.urls')),
    path('baskets/', include('basketapp.urls', namespace = 'baskets')),
    path('admin-staff/', include('adminapp.urls', namespace = 'admin-staff')),
    path('order/', include('ordersapp.urls', namespace = 'order')),

    # path('text_context/', mainapp_views.text_context),

    path('', include('social_django.urls', namespace = 'social')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]
