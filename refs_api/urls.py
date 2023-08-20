from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import get_jwt_token, register, MyProfileViewSet, ProfilesViewSet

app_name = 'refs_api'

router = DefaultRouter()
router.register(r'all_profiles', ProfilesViewSet, basename='all_profiles')
router.register(r'my_profile', MyProfileViewSet, basename='my_profile')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', get_jwt_token, name='get_jwt_token'),
    path('v1/auth/signup/', register, name='signup')
]
