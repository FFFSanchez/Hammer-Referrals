from refs_api.models import MyUser

from django.contrib.auth.backends import ModelBackend


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password.

    """
    def authenticate(self, username=None):
        try:
            print('ssss')
            return MyUser.objects.get(phone=username)
        except MyUser.DoesNotExist:
            print('fff')
            return None

    def get_user(self, user_id):
        try:
            print('aaa')
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            print('ccc')
            return None
