from django import forms
from django.core.exceptions import ValidationError

from refs_api.validators import phone_regex

from .models import Profile


class SubmitForm(forms.Form):
    """ Here enter confirm code while signup """

    code = forms.CharField(max_length=4, help_text='Enter your submit code')


class SignUpForm(forms.Form):
    """ Here enter phone number while signup """

    phone = forms.CharField(
        max_length=25,
        validators=[phone_regex],
        help_text='Enter your phone number'
    )


class InvitedByForm(forms.Form):
    """ Here enter code of your inviter in your profile """

    invited_by = forms.CharField(
        max_length=25,
        help_text='Enter ref code of your inviter'
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request') if 'request' in kwargs else None
        super(InvitedByForm, self).__init__(*args, **kwargs)

    def clean_invited_by(self):
        data = self.cleaned_data['invited_by']
        profile = Profile.objects.get(user=self.request.user)

        try:
            inviter_profile = Profile.objects.get(my_ref_code=data)

        except Exception:
            raise ValidationError("No such user registered!")

        if inviter_profile == profile:
            raise ValidationError("You cant be invited by yourself!")

        if inviter_profile.recommended_by == profile.user:
            raise ValidationError("Cross referrals Are not allowed!")

        return data
