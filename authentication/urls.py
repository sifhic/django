from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from .views import account_activation_sent,account_invite,invite_accept
from authentication import views as core

app_name = 'authentication'

urlpatterns = [

    url(r'^login/$', core.LoginView.as_view(), name='login'),
    url(r'^signup/$', core.RegisterView.as_view(), name='signup'),
    url(r'^invite/$', account_invite, name='invite'),
    url(r'^invite/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/accept$',
        invite_accept,
        name='invite-accept'),
    url(r'^logout/$', core.LogoutView.as_view(), name='logout'),
    url(r'^profile/$', core.AccountSettingsView.as_view(), name='settings'),

    url(r'^password_reset/$',
        auth_views.PasswordResetView.as_view(**{
            'template_name': 'authentication/registration/password_reset_form.html',
            'from_email': 'salesleadgen@mohit-development.website',
            'email_template_name': 'authentication/registration/password_reset_email.html',
            'subject_template_name': 'authentication/registration/password_reset_subject.txt',
            'success_url':reverse_lazy('authentication:password_reset_done')
        }),
        name='password_reset'
        ),
    url(r'^password_reset/done/$',
        auth_views.PasswordResetDoneView.as_view(
            **{'template_name': 'authentication/registration/password_reset_done.html'}),
        name='password_reset_done'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core.activate, name='activate'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(**{
            'success_url': reverse_lazy('authentication:password_reset_complete'),
            'template_name': 'authentication/registration/password_reset_confirm.html'
        }),
        name='password_reset_confirm'
        ),
    url(r'^reset/done/$',
        auth_views.PasswordResetCompleteView.as_view(**{
            'template_name': 'authentication/registration/password_reset_complete.html'
        }),
        name='password_reset_complete'),
    url(r'^account_activation_sent/$', account_activation_sent, name='account_activation_sent'),

]
