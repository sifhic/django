from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.contrib.auth import get_user_model

from django.utils.translation import gettext, gettext_lazy as _


class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name','last_name', 'password1', 'password2',)

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification. (also to catch typos)"),
    )

    first_name = forms.CharField(required=False)


    # def _post_clean(self):
    #     super()._post_clean()
    #     # Validate the email hasn't been used by an account yet
    #     #  after self.instance is updated with form data
    #     # by super().
    #     email = self.cleaned_data.get("email")
    #     if Email.objects.filter().exists():
    #         self.add_error('email', error)


class AccountSettingsForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name','last_name','company', 'password1', 'password2',)

    first_name = forms.CharField(required=False)



class SignInForm(AuthenticationForm):

    username = UsernameField(
        max_length=254,
        label='Username or Email' # the form is extended to edit this label
    )


class AccountInviteForm(forms.Form):
    email = forms.EmailField(help_text='User Email',required=True)
