from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone


class MyUserManager(BaseUserManager):
    """ Custom Manager without password Only phone """

    def create_user(self, phone, password=None):
        """ Create Common User """

        user = self.model(
            phone=phone,
        )

        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        """ Create User and add admin's perms. Requires password """

        user = self.create_user(phone)
        user.is_staff = True
        user.is_superuser = True

        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    """ Custom User model with only nessessary fields """

    phone = models.CharField(
        unique=True,
        max_length=13
    )

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = MyUserManager()
    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.phone


class ConfirmCodePair(models.Model):
    """ Model for confirmation codes """

    phone = models.CharField(
        unique=True,
        max_length=150
    )
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(
        'Created_at', auto_now_add=True
    )

    def __str__(self):
        return f'User phone: {self.phone}, Conf code {self.code}'
