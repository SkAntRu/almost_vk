from functools import wraps
from additional_functions import is_social_auth


def is_vk_auth_decorator(view_func):
    """
    Add to user parameter social

    Input:
        view_func
    """
    @wraps(view_func)
    def new_view_func(request, *args, **kwargs):
        request = is_social_auth(request, provider='vk-oauth2')
        response = view_func(request, *args, **kwargs)
        return response
    return new_view_func
