from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,11}$',
    message="Phone number must be entered in the format: '+999999999'. "
            "Up to 11 digits allowed."
)
