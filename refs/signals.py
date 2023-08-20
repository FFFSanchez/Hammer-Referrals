from django.db.models.signals import post_save
from django.dispatch import receiver

from refs_api.models import MyUser

from .models import Profile


@receiver(post_save, sender=MyUser)
def post_save_create_profile(sender, instance, created, *args, **kwargs):
    """ When new User is created - automaticaly create Profile for him """

    if created:
        Profile.objects.create(user=instance, phone=instance.phone)

# Also can be realised in views perform create method when User saved
