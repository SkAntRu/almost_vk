from . import views
from django.urls import path
# from django.contrib.auth import views as auth_views

app_name = 'vk_login'
urlpatterns = [
    path('', views.index, name='index'),
    path("logout/", views.logout_view, name="logout"),
]
