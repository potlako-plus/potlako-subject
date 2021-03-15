from django.core.exceptions import ValidationError

from edc_base.utils import get_utcnow


def datetime_not_now(value):
    if value == get_utcnow():
        raise ValidationError('Cannot be current date and time')


def date_not_now(value):
    if value == get_utcnow().date():
        raise ValidationError('Cannot be today\'s date')


def identity_check(value):
    if len(str(value)) != 9:
        raise ValidationError('The identity number must be '
                              'exactly 9 digits.')


def age_check(value):
    if value < 30:
        raise ValidationError('Participant is less than 30 years old, cannot be enrolled '
                              'into the study.')
