import logging

from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth import login
from authentication.forms import SignInForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.http import is_safe_url
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView

from .forms import SignUpForm,AccountSettingsForm,AccountInviteForm
from django.contrib.auth import get_user_model
from authentication.models import Email
from django.conf import settings
import django

Account = get_user_model()

# Create your views here.
lgr = logging.getLogger(__name__)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        primary_email = Email.objects.get(email=user.email)
        primary_email.is_verified = True
        primary_email.save()

        login(request, user,backend='authentication.backends.username_or_email.UsernameEmailBackend')
        return redirect(settings.INDEX_URL)
    else:
        return render(request, 'authentication/account_activation_invalid.html')


def account_activation_sent(request):
    return render(request, 'authentication/account_activation_sent.html')


class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    template_name = 'authentication/login.html'
    # template_name = 'partials/dash_menu.html'
    # template_name = 'web/dash_test.html'

    form_class = SignInForm
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(ensure_csrf_cookie)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        # request.session.set_test_cookie()
        # lgr.info("Test Cookie Set")
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)

        return context


    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        # if self.request.session.test_cookie_worked():
        #    lgr.info('test cookie worked')
        #    self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, allowed_hosts=self.request.get_host()):
            redirect_to = reverse(settings.INDEX_URL)
        return redirect_to


class RegisterView(FormView):
    """
    Provides the ability to register user with a username and password
    """
    template_name = 'authentication/register.html'

    form_class = SignUpForm
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password', 'password2'))
    @method_decorator(csrf_protect)
    @method_decorator(ensure_csrf_cookie)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        # request.session.set_test_cookie()
        # lgr.info("Test Cookie Set")
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()


        # print('form save')

        if not user.is_superuser:
            # TODO from organizations.utils import create_organization
            #
            # organisation = create_organization(
            #     user,
            #     form.cleaned_data.get('organization','Rafikihost'),
            #     org_user_defaults={'is_admin': True}
            # )
            pass

        # auth_login(self.request, user)

        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        kwargs = {
            'url': redirect_to,
            'allowed_hosts':settings.ALLOWED_HOSTS
        }
        # Django 1.11+ allows us to require https, too.
        if django.VERSION >= (1, 11):
            kwargs['require_https'] = self.request.is_secure()
        # Django 2.1 drops support for the `host` kwarg.
        if django.VERSION <= (2, 0):
            kwargs['host'] = self.request.get_host()

        if not is_safe_url(**kwargs):
            redirect_to = reverse('authentication:account_activation_sent')
        return redirect_to


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    template_name = 'core/logout.html'
    pattern_name = settings.INDEX_URL

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class AccountSettingsView(FormView):
    """
    Provides the ability to register user with a username and password
    """
    template_name = 'authentication/profile.html'
    # success_url = '/account_activation_sent/'
    form_class = AccountSettingsForm
    redirect_field_name = REDIRECT_FIELD_NAME

    # todo finish
    # 'basic_information_form': basic_information_form,
    # 'login_information_form': login_information_form,

    # todo also finish
    # basic_information_form = AccountSettingsForm()
    # login_information_form = AccountSettingsForm()

    def dispatch(self, request, *args, **kwargs):
        return super(AccountSettingsView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        return super(AccountSettingsView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        kwargs = {
            'url': redirect_to,
            'allowed_hosts':settings.ALLOWED_HOSTS
        }
        # Django 1.11+ allows us to require https, too.
        if django.VERSION >= (1, 11):
            kwargs['require_https'] = self.request.is_secure()
        # Django 2.1 drops support for the `host` kwarg.
        if django.VERSION <= (2, 0):
            kwargs['host'] = self.request.get_host()

        if not is_safe_url(**kwargs):
            redirect_to = self.success_url
        return redirect_to

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import random
import string


def random_string(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def account_invite(request):
    if request.method == "POST":
        lgr.info(request.POST)
        form = AccountInviteForm(request.POST)
        if form.is_valid():
            password = random_string()

            user = Account()
            user.is_staff = False
            user.is_superuser = False
            user.is_active = False
            user.email = form.cleaned_data['email']
            user.set_password(password)
            user.save()

            if settings.PORT == 443 or settings.PORT == 80:
                PORT = ''
            else:
                PORT = (':{}'.format(settings.PORT) if settings.PORT else '')

            subject = 'Activate Your {} Account'.format(settings.PROJECT_NAME)
            message = render_to_string('authentication/account_invite_email.html', {
                'user': user,
                'protocol': settings.PROTOCOL,
                'domain': settings.HOST + PORT,
                'password': password,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
                'token': default_token_generator.make_token(user),
            })

            user.email_user(subject, message, from_email='noreply@'+settings.DOMAIN)

            return redirect('/')
        else:
            lgr.error('account invite form error')
            lgr.error(form.errors)

    else:
        form = AccountInviteForm()

    return render(request, 'authentication/account_invite.html',{
        'form':form
    })


def invite_accept(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user,backend='authentication.backends.username_or_email.UsernameEmailBackend')
        return redirect(settings.INDEX_URL)

    else:
        return render(request, 'authentication/account_activation_invalid.html')
