from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from authapp.models import User
from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm, AdminProductCategory
from mainapp.models import ProductCategory

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'adminapp/index.html')


class UsersListView(ListView):
    model = User
    template_name = 'adminapp/admin-users-read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UsersListView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users(request):
#     context = {
#         'users': User.objects.all(),
#     }
#     return render(request, 'adminapp/admin-users-read.html', context)

class UsersCreateView(CreateView):
    model = User
    template_name = 'adminapp/admin-users-create.html'
    success_url = reverse_lazy('admin-staff:admin_users')
    form_class = UserAdminRegisterForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UsersCreateView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegisterForm(data = request.POST, files = request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin-staff:admin_users'))
#         else:
#             print(form.errors)
#     else:
#         form = UserAdminRegisterForm()
#     context = {'form': form}
#     return render(request, 'adminapp/admin-users-create.html', context)

class UsersUpdateView(UpdateView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('admin-staff:admin_users')
    form_class = UserAdminProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'GeekShop - Редактирование пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UsersUpdateView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_update(request, user_id):
#     user = User.objects.get(id = user_id)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(data = request.POST, files = request.FILES, instance = user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin-staff:admin_users'))
#     else:
#         form = UserAdminProfileForm(instance = user)
#
#     context = {'form': form, 'user': user}
#     return render(request, 'adminapp/admin-users-update-delete.html', context)


class UserDeleteView(DeleteView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('admin-staff:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_remove(request, user_id):
#     user = User.objects.get(id = user_id)
#     user.is_active = False
#     user.save()
#     return HttpResponseRedirect(reverse('admin-staff:admin_users'))


@user_passes_test(lambda u: (u.is_superuser or u.is_staff))
def admin_catalogs_read(request):
    contex = {
        'titlepage': 'каталог товаров',
        'catalogs': ProductCategory.objects.all(),
    }

    return render(request, 'adminapp/admin_catalogs_read.html', context = contex)


@user_passes_test(lambda u: (u.is_superuser or u.is_staff))
def admin_catalogs_create(request):
    if request.method == 'POST':
        form = AdminProductCategory(data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin-staff:admin_catalogs_read'))
    else:
        form = AdminProductCategory()

    context = {'form': form}
    return render(request, 'adminapp/admin-catalogs-create.html', context)


@user_passes_test(lambda u: (u.is_superuser or u.is_staff))
def admin_catalogs_update(request, cat_id):
    catalog = ProductCategory.objects.get(id = cat_id)
    if request.method == 'POST':
        form = AdminProductCategory(data = request.POST, instance = catalog)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin-staff:admin_catalogs_read'))
    else:
        form = AdminProductCategory(instance = catalog)

    context = {'form': form, 'catalog': catalog}
    return render(request, 'adminapp/admin-catalogs-update-delete.html', context)


@user_passes_test(lambda u: (u.is_superuser or u.is_staff))
def admin_catalogs_remove(request, cat_id):
    catalog = ProductCategory.objects.get(id = cat_id)
    catalog.delete()

    return HttpResponseRedirect(reverse('admin-staff:admin_catalogs_read'))
