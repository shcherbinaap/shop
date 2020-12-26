from django import forms

from authapp.forms import UserRegisterForm, UserProfileForm
from authapp.models import User
from mainapp.models import ProductCategory


class UserAdminRegisterForm(UserRegisterForm):
    avatar = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'avatar')

    def __init__(self, *args, **kwargs):
        super(UserAdminRegisterForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs['class'] = 'custom-file-input'


class UserAdminProfileForm(UserProfileForm):

    def __init__(self, *args, **kwargs):
        super(UserAdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = False
        self.fields['email'].widget.attrs['readonly'] = False


class AdminProductCategory(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super(AdminProductCategory, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control py-4'
        self.fields['description'].widget.attrs['class'] = 'form-control py-4'