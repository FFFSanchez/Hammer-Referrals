from django.contrib import admin

from refs.models import Profile

from .models import ConfirmCodePair, MyUser


class MyUserAdmin(admin.ModelAdmin):
    list_display = (
        'phone',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined'
    )
    search_fields = ('phone',)
    list_filter = ('is_staff',)
    empty_value_display = '-date_joined-'


class ConfirmCodePairAdmin(admin.ModelAdmin):
    list_display = (
        'phone',
        'code',
        'created_at'
    )
    search_fields = ('phone',)
    empty_value_display = '-date_joined-'


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone',
        'my_inviter',
        'recommended_by',
        'my_ref_code',
        'created_at',
        'updated_at'
    )
    search_fields = ('phone',)
    list_filter = ('created_at',)
    empty_value_display = '-nothing-'


admin.site.register(Profile, ProfileAdmin)
admin.site.register(ConfirmCodePair, ConfirmCodePairAdmin)
admin.site.register(MyUser, MyUserAdmin)
