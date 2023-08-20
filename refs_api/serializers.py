from rest_framework import serializers

from refs.models import Profile

from .models import MyUser
from .validators import phone_regex


class RegisterDataSerializer(serializers.ModelSerializer):
    """ Signup Users """

    phone = serializers.CharField(
        max_length=150,
        validators=[phone_regex]
    )

    class Meta:
        fields = ('phone',)
        model = MyUser


class TokenSerializer(serializers.Serializer):
    """ Get Access Token by confirmation code """

    phone = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.Serializer):
    """ Refs users serializer """
    phone = serializers.CharField()

    class Meta:
        model = MyUser
        fields = ('phone',)


class ProfileSerializer(serializers.ModelSerializer):
    """ Profile GET all, GET my and PATCH my """

    my_refs = serializers.SerializerMethodField()

    def get_my_refs(self, obj):

        refs = MyUser.objects.filter(id__in=obj.user.ref_by.all())
        return UserSerializer(refs, many=True).data

    def validate_my_inviter(self, value):

        if not Profile.objects.filter(my_ref_code=value).exists():
            raise serializers.ValidationError(
                'User with this invite code doesnt exist!'
            )
        if self.instance.my_ref_code == value:
            raise serializers.ValidationError(
                'You cant sign your ref code!'
            )
        if self.instance.my_inviter:
            raise serializers.ValidationError(
                'You can sign your inviter only once!'
            )
        inviter_profile = Profile.objects.get(my_ref_code=value)
        if inviter_profile.recommended_by == self.instance.user:
            raise serializers.ValidationError(
                "Cross referrals Are not allowed!"
            )

        return value

    class Meta:
        model = Profile
        fields = (
            'phone',
            'my_refs',
            'my_inviter',
            'my_ref_code',
            'created_at',
        )
        read_only_fields = (
            'phone',
            'my_refs',
            'my_ref_code',
            'created_at',
        )
