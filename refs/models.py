from django.db import models

from refs_api.models import MyUser

from .utils import generate_ref_code


class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, null=True, blank=True)

    my_inviter = models.CharField(max_length=50, blank=True, null=True)

    recommended_by = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='ref_by',
        blank=True,
        null=True
    )
    my_ref_code = models.CharField(max_length=12, blank=True)
    created_at = models.DateTimeField(
        'Created_at', auto_now_add=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ('Profile')
        verbose_name_plural = ('Profiles')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.phone} - {self.my_ref_code}'

    def get_recommended_profiles(self):  # Optimize
        qs = Profile.objects.all()
        my_recs = [p for p in qs if p.recommended_by == self.user]

        return my_recs

    def save(self, *args, **kwargs):
        if self.my_ref_code == '':
            code = generate_ref_code()
            self.my_ref_code = code
        super().save(*args, **kwargs)
