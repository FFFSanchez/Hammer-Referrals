from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils import timezone

from hammer_refs.settings import FAKE_CONFIRM
from refs_api.models import ConfirmCodePair, MyUser

from .forms import InvitedByForm, SignUpForm, SubmitForm
from .models import Profile
from .utils import generate_confirmation_code


def main_view(request, *args, **kwargs):
    """ Render main page and SignUp Form """

    form = SignUpForm(request.POST or None)

    if form.is_valid():

        phone = form.cleaned_data.get('phone')
        print(phone)
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

        request.session['phone'] = phone
        if FAKE_CONFIRM:
            request.session['code'] = confirmation_code

        return redirect('refs:submit')
    context = {
        'form': form,
        'card_title': 'Home'
    }

    return render(request, 'main.html', context)


def submit_view(request, *args, **kwargs):
    """ Render /submit page """

    form = SubmitForm(request.POST or None)
    messages.add_message(
        request,
        messages.INFO,
        message="Confirmation Code was forwarded to you"
    )
    if FAKE_CONFIRM:
        messages.add_message(
            request,
            messages.INFO,
            message=request.session['code']
        )
    phone = request.session['phone']

    if form.is_valid():

        confirmation_code = form.cleaned_data.get('code')
        print(confirmation_code)

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

            login(request, user)

            return redirect('refs:main-view')
        else:
            messages.error(request, "This submit code is invalid!")
    context = {
        'form': form,
        'card_title': 'Submit Code'
    }
    return render(request, 'submit.html', context)


def my_profile_view(request):
    """ Render /profile page """

    profile = Profile.objects.get(user=request.user)
    my_phone = profile.phone
    my_recs = profile.get_recommended_profiles()
    my_invate_code = profile.my_ref_code
    i_was_invited_by = profile.recommended_by

    form = InvitedByForm(request.POST or None, request=request)
    if form.is_valid():
        invite_code = form.cleaned_data.get('invited_by')
        inviter_profile = Profile.objects.get(my_ref_code=invite_code)

        profile.recommended_by = inviter_profile.user
        profile.my_inviter = inviter_profile.phone
        profile.save()

        return redirect('refs:profile')

    context = {
        'form': form,
        'my_phone': my_phone,
        'my_recs': my_recs,
        'my_invate_code': my_invate_code,
        'i_was_invited_by': i_was_invited_by,
        'card_title': 'My Profile'
    }
    return render(request, 'profile.html', context)
