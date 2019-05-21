from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import resolve
from django.conf import settings

# from django.core.exceptions import MiddlewareNotUsed
# from re import compile
import logging

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

lgr = logging.getLogger(__name__)

# from django.utils.deprecation import MiddlewareMixin
LOGIN_URL = reverse(settings.LOGIN_URL)

EXEMPT_URLS = []
if hasattr(settings, 'LOGIN_DEFAULT_EXEMPT_URLS'):
    EXEMPT_URLS += [expr for expr in settings.LOGIN_DEFAULT_EXEMPT_URLS]

REDIRECT_URLS = [settings.LOGIN_URL]
if hasattr(settings, 'LOGIN_SESSION_REDIRECT_HOME_URLS'):
    REDIRECT_URLS += [expr for expr in settings.LOGIN_SESSION_REDIRECT_HOME_URLS]

if hasattr(settings, 'LOGIN_DEFAULT_PERMISSIVE'):
    if not settings.LOGIN_DEFAULT_PERMISSIVE:
        EXEMPT_URLS += REDIRECT_URLS


class AuthenticationRequiredMiddleware(MiddlewareMixin):
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).
    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """

    def process_request(self, request):
        lgr.info('AuthenticationRequiredMiddleware')
        lgr.info('LOGIN_DEFAULT_PERMISSIVE : {}'.format(settings.LOGIN_DEFAULT_PERMISSIVE))

        assert_error_message = '''
        The Login Required middleware requires authentication middleware to be installed. 
        Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.auth.middleware.AuthenticationMiddleware'. 
        If that doesn't work, 
        ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes 'django.core.context_processors.auth'
        '''

        assert hasattr(request, 'user'), assert_error_message
        path = request.path_info
        lgr.info('path : {}'.format(path))

        # todo catch exception, django.urls.exceptions.Resolver404:
        # todo optimize, check if accessible from request
        view_name = resolve(path).view_name
        lgr.info('view name : {}'.format(view_name))

        if not request.user.is_authenticated:
            lgr.info('request not authenticated')
            lgr.info('EXEMPT_URLS : {}'.format(EXEMPT_URLS))
            if settings.LOGIN_DEFAULT_PERMISSIVE:
                if view_name in EXEMPT_URLS:
                    lgr.info('view name : {}'.format(view_name))
                    # if any(m.match(path) for m in EXEMPT_URLS):
                    next = ('?next={}'.format(settings.BASE_PATH+path) if path else '')
                    return HttpResponseRedirect(settings.BASE_PATH+LOGIN_URL + next)

            else:
                if view_name not in EXEMPT_URLS:
                    # if not any(m.match(path) for m in EXEMPT_URLS):
                    next = ('?next={}'.format(settings.BASE_PATH + path) if path else '')
                    return HttpResponseRedirect(settings.BASE_PATH+LOGIN_URL + next)

        else:
            lgr.info('request authenticated')
            lgr.info('REDIRECT_URLS : {}'.format(REDIRECT_URLS))
            if view_name in REDIRECT_URLS:
                #if path and any(m.match(path) for m in REDIRECT_URLS):
                return HttpResponseRedirect(reverse(settings.INDEX_URL))


class RedirectAdminMiddleware(MiddlewareMixin):
    """
    Middleware class that re-redirects a superuser to the superuser site
    """
    def process_request(self, request):
        path = request.path_info.lstrip('/')
        if request.user.is_superuser:
            if not compile(settings.SUPERUSER_DASHBOARD).match(path):
                return HttpResponseRedirect(settings.SUPERUSER_DASHBOARD)
        elif compile(settings.SUPERUSER_DASHBOARD).match(path):
            return HttpResponseRedirect(settings.INDEX_URL)
