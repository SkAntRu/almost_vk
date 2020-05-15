import urllib.request
import json
from social_django.models import UserSocialAuth


def is_social_auth(request, provider: str) -> object:
    """Check that request.user has account in provider

    Input:
        request
        provider: str. For example = ''vk-oauth2''

    Return
        request
    """
    user = request.user
    if request.user.is_authenticated:
        try:
            social = user.social_auth.get(provider=provider)
        except UserSocialAuth.DoesNotExist:
            social = None
    else:
        social = None
    request.user.social = social
    return request


def get_vk_friends(access_token: str) -> object:
    """
    Invoke social_core.backends.vk.vk_api to get list of 5 friends of uid vk user

    template_url = '{url}/method/{method}?{parameters}&access_token={access_token}&v={api_version}'
    """
    template_url = '{url}/method/{method}?{parameters}&access_token={access_token}&v={api_version}'
    url = 'https://api.vk.com/'
    method = 'friends.get'
    api_version = '5.52'
    friends_count = '5'
    order = 'random'
    additional_fields = [
        'first_name',
        'last_name',
        'photo_100'
    ]
    additional_fields = ','.join(param for param in additional_fields)
    parameters = {
       'count': friends_count,
       'fields': additional_fields,
       'order': order,
    }
    parameters = '&'.join(param + '=' + value for param, value in parameters.items())
    request_url = template_url.format(
        url=url,
        method=method,
        parameters=parameters,
        access_token=access_token,
        api_version=api_version,
    )
    request = urllib.request.Request(request_url)
    try:
        response = urllib.request.urlopen(request, timeout=5)
    except urllib.error.HTTPError:
        # log error
        return None
    response = response.read().decode('utf-8')
    response = json.loads(response)
    response = response['response']['items']
    return response
