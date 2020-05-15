from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from decorators import is_vk_auth_decorator
from additional_functions import get_vk_friends


@is_vk_auth_decorator
def index(request):
    """
    view to main page
    """
    template = 'vk_login/not_authentificated.html'
    if request.user.social:
        # request.user.social['friends'] = get_vk_friends(request.user.social.extra_data['access_token'])
        request.user.social.friends = get_vk_friends(request.user.social.extra_data['access_token'])
        template = 'vk_login/authentificated.html'
    return render(request, template)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
