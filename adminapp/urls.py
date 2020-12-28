from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name = 'index'),
    path('users/', adminapp.admin_users, name = 'admin_users'),
    path('users/create/', adminapp.admin_users_create, name = 'admin_users_create'),
    path('users/update/<int:user_id>/', adminapp.admin_users_update, name = 'admin_users_update'),
    path('users/remove/<int:user_id>/', adminapp.admin_users_remove, name = 'admin_users_remove'),
    path('catalogs/', adminapp.admin_catalogs_read, name = 'admin_catalogs_read'),
    path('catalogs/create/', adminapp.admin_catalogs_create, name = 'admin_catalogs_create'),
    path('catalogs/update/<int:cat_id>', adminapp.admin_catalogs_update, name = 'admin_catalogs_update'),
    path('catalogs/remove/<int:cat_id>', adminapp.admin_catalogs_remove, name = 'admin_catalogs_remove'),
]
