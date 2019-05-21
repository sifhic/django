from django.contrib.auth.models import AbstractUser, UserManager
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import gettext_lazy as _

from django.conf import settings
# Create your models here.


class AccountManager(UserManager):
    use_in_migrations = True

    # def _create_user(self, email, password, **extra_fields):
    #     if not email:
    #         raise ValueError('Email address must be provided')
    #
    #     if not password:
    #         raise ValueError('Password must be provided')
    #
    #     email = self.normalize_email(email)
    #     user = self.model(email=email, **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if not email:
            raise ValueError('The given email must be set')

        # if email:
        #     try:Email.objects.get_or_create()

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not email:
            raise ValueError('The given email must be set')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_email_new(value):
    if Email.objects.filter(email=value).exists():
        raise ValidationError(
            _("A user with that email already exists."),
            params={'value': value},
        )
    # TODO what if the email is_verified

# @python_2_unicode_compatible
# class Institution(models.Model):
#     name = models.CharField(max_length=100,default='Rafikihost')
#

@python_2_unicode_compatible
class User(AbstractUser):
    objects = AccountManager()
    email = models.EmailField(
        _('primary email'),
        blank=False,
        unique=True,
        validators=[validate_email_new],
        help_text='Will be validated. <br> You can validate more emails for Login after Registering'
    )

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    username = models.CharField(
        _('username'),
        max_length=150,
        # widget=forms.TextInput(attrs={'autofocus': True}),
        unique=True,
        help_text=_('Required. <br> 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    phone = models.CharField(max_length=8, unique=True, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='profiles/images/%d')  # todo include current date

    # created_at = this is already here as date_joined
    updated_at = models.DateTimeField(auto_now=True)



@python_2_unicode_compatible
class Email(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')

    email = models.EmailField(_('email address'), blank=False, unique=True)
    is_verified = models.BooleanField('email verified', default=False)  # account email is valid
    # is_blacklisted = models.BooleanField('email blacklisted',default=False)

    def __str__(self):
        return  '{} - {}'.format(self.user, self.email)


@receiver(post_save, sender=User)
def create_primary_email(sender, instance, created, **kwargs):
    if created:
        Email.objects.create(user=instance,email=instance.email)


@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    if created and \
            not instance.is_superuser: # don't send emails for `createsuperuser` management command
        if settings.PORT == 443 or settings.PORT == 80:
            PORT = ''
        else:
            PORT = (':{}'.format(settings.PORT) if settings.PORT else '')

        subject = 'Activate Your {} Account'.format(settings.PROJECT_NAME)
        message = render_to_string('authentication/account_activation_email.html', {
            'user': instance,
            'protocol': settings.PROTOCOL,
            'domain': settings.HOST+PORT,
            # todo warn if settings not implemented or use current request settings
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)).decode('utf-8'),
            'token': default_token_generator.make_token(instance),
        })

        instance.email_user(subject, message, from_email='salesleadgen@mohit-development.website')
