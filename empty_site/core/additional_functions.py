import urllib.request
import json
from datetime import datetime
from social_django.models import UserSocialAuth
from social_django.utils import load_strategy
import typing


def check_and_update_vk_token(social: object,
                              request: object,
                              ) -> object:
    """
    Check if vk token is valid and has not expired

    Input:
        social: object. Instance of Social-auth

    Return
        social: object.

    If token is valid - return True
    If token expired - delete social instance and return False
    """
    token_expires = float(social.extra_data['expires'])
    token_auth_time = float(social.extra_data['auth_time'])
    linux_timestamp_now = datetime.now().timestamp()
    if (token_auth_time + token_expires) < linux_timestamp_now:
        strategy = load_strategy(request)
        social.refresh_token(strategy)
    return social


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

    if social:
        social = check_and_update_vk_token(social=social, request=request)
    request.user.social = social
    return request


def get_vk_friends(access_token: str,
                   friends_count: typing.Union[str, int] = '5',
                   ) -> typing.List[dict]:
    """
    Invoke social_core.backends.vk.vk_api to get list of 5 friends of uid vk user

    template_url = '{url}/method/{method}?{parameters}&access_token={access_token}&v={api_version}'

    Input:
        access_token: str
        friends_count: str = '5'

    Return:
        friend_list: typing.List[dict]
    """
    friends_count = str(friends_count)
    template_url = '{url}/method/{method}?{parameters}&access_token={access_token}&v={api_version}'
    url = 'https://api.vk.com/'
    method = 'friends.get'
    api_version = '5.52'
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
    friends_list = response['response']['items']
    if len(friends_list) < 5:
        for friend in friends_list:
            if friend['first_name'] == 'DELETED':
                friends_list.remove(friend)
        return friends_list
    else:
        for friend in friends_list:
            if friend['first_name'] == 'DELETED':
                friends_list.remove(friend)
        # if we remove DELETED friends from friends_list -> len(friends_list)<5
        # So - or we render < 5 friends or execute get_vk_friends again to fill freinds_list up to 5
        # Lets fill friends_list up to 5
        # Recursion =)
        while len(friends_list) < int(friends_count):
            more_active_friends = get_vk_friends(access_token=access_token,
                                                 friends_count=len(friends_count) - len(friends_list),
                                                 )
            for new_friend in more_active_friends:
                if new_friend not in friends_list:
                    friends_list.append(more_active_friends)

    return friends_list
