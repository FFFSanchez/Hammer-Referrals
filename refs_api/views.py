from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from hammer_refs.settings import FAKE_CONFIRM
from refs.models import Profile
from refs.utils import generate_confirmation_code

from .models import ConfirmCodePair, MyUser
from .permissions import IsAdmin
from .serializers import (ProfileSerializer, RegisterDataSerializer,
                          TokenSerializer)


@permission_classes([permissions.AllowAny])
@api_view(['POST'])
def register(request):
    """ SignUp user and send confirmation code """

    serializer = RegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    phone = serializer.data.get('phone')

    confirmation_code = generate_confirmation_code()

    ConfirmCodePair.objects.filter(phone=phone).delete()
    ConfirmCodePair.objects.create(phone=phone, code=confirmation_code)

    import time
    time.sleep(2)

    send_mail(
        subject='SMS confirmation code',
        message=f'Confirmation code: {confirmation_code}',
        from_email=settings.TOKEN_EMAIL,
        recipient_list=[phone],
    )
    print(serializer.data)
    info_msg = {'info': 'Confirmation Code was forwarded to you'}
    info_msg.update(serializer.data)

    if FAKE_CONFIRM:
        code = {'Your code': confirmation_code}
        info_msg.update(code)

    return Response(info_msg)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    """ Send Token to Confirmed User and Create User if he is new """

    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    phone = serializer.validated_data['phone']
    confirmation_code = serializer.validated_data['confirmation_code']

    try:
        confirm_pair = ConfirmCodePair.objects.get(
            phone=phone,
            code=confirmation_code
        )
    except ConfirmCodePair.DoesNotExist:
        confirm_pair = None

    if confirm_pair:
        user = MyUser.objects.get_or_create(phone=phone)[0]
        user.last_login = timezone.now()
        user.save()

        token = AccessToken.for_user(user)

        return Response({
            'info': [
                'Phone Confirmed',
                'Use this token for authentication'
            ],
            'token': str(token)
            })
    return Response(
        {'confirmation_code': ['This submit code is invalid!']},
        status=status.HTTP_400_BAD_REQUEST,
    )


class MyProfileViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    View for /profile endpoint.
    Allow GET user profile and PATCH My_inviter field
    """

    http_method_names = ['get', 'patch']
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer
    pagination_class = None

    def get_queryset(self):
        new_queryset = Profile.objects.filter(user=self.request.user)
        return new_queryset

    def patch(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            my_inviter = serializer.validated_data.get('my_inviter')
            inviter_profile = Profile.objects.get(my_ref_code=my_inviter)
            profile.recommended_by = MyUser.objects.get(
                id=inviter_profile.user_id
            )
            profile.my_inviter = inviter_profile.phone
            profile.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfilesViewSet(viewsets.ModelViewSet):
    """ Any Profiles Operations for Admin only """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAdmin,)  # is stuff
