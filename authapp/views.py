from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from authapp.models import User
from basketapp.models import Basket


def send_verify_email(user):
    # TODO сделать отправку писем на реальную почту и приема ссылки с нее

    verify_link = reverse('authapp:verify', args = [user.email, user.activation_key])

    subject = f'подтверждение учетной записи {user.username}'
    message = f'Для подтверждения пройдите по ссылке {settings.DOMAIN}{verify_link}'

    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently = False)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email = email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            activation_key = None
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
    except Exception as ex:
        return HttpResponseRedirect(reverse('main'))

# @csrf_exempt
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username = username, password = password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main'))
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'authapp/login.html', context = context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data = request.POST)
        if form.is_valid():
            user = form.save()
            if send_verify_email(user):
                messages.success(request,
                                 'Вы успешно зарегистрировались!Ссылка для активации акаунта выслана Вам на почту!')

            return HttpResponseRedirect(reverse('authapp:login'))

    else:
        form = UserRegisterForm()

    context = {'form': form}

    return render(request, 'authapp/register.html', context = context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data = request.POST, files = request._files, instance = request.user)
        profile_form = UserProfileEditForm(data = request.POST, instance = request.user.userprofile)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('authapp:profile'))
    else:
        form = UserProfileForm(instance = request.user)
        profile_form = UserProfileEditForm(instance = request.user.userprofile)
    context = {
        'form': form,
        'profile_form': profile_form,
        'baskets': Basket.objects.filter(user = request.user)
    }
    return render(request, 'authapp/profile.html', context = context)
