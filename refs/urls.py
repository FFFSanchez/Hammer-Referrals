from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import main_view, my_profile_view, submit_view


app_name = 'refs'

urlpatterns = [
    path('', main_view, name='main-view'),
    path('submit/', submit_view, name='submit'),
    path('my_profile/', my_profile_view, name='profile'),
    path(
        'logout/',
        LogoutView.as_view(template_name='logged_out.html'),
        name='logout')
]
