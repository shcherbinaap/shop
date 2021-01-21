import datetime
from collections import OrderedDict
from urllib.parse import urlunparse, urlencode
from urllib.request import urlopen

import requests
from django.conf import settings
from django.core.files.base import ContentFile

from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    # api_url = f"https://api.vk.com/methodod/users.get/user_ids={settings.SOCIAL_AUTH_VK_OAUTH2_KEY}" \
    #           f"&fields=bdate" \
    #           f"&access_token={response['access_token']}" \
    #           f"&v=5.126"

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields = ','.join(('bdate', 'sex', 'country',
                                                                   'about', 'photo_50')),
                                                access_token = response['access_token'],
                                                v = '5.92')),
                          None
                          ))

    resp = requests.get(api_url)

    if resp.status_code != 200:
        return
    data = resp.json()['response'][0]

    # print(data)

    if data['sex'] == 2:
        user.userprofile.gender = UserProfile.MALE
    elif data['sex'] == 1:
        user.userprofile.gender = UserProfile.FEMALE

    if data['about']:
        user.userprofile.aboutMe = data['about']


    if 'bdate' in data:
        bdate = datetime.datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')



    if data['photo_50']:
        photo_url = data['photo_50']
        photo_content = urlopen(photo_url)
        photo_name = str(user.id)
        user.avatar.save(photo_name, ContentFile(photo_content.read()))



    user.save()
