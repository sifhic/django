from django import forms
from django.utils.translation import ugettext_lazy as _

from core.models import SampleModel

import logging
from django.conf import settings

lgr = logging.getLogger(__name__)



class SampleModelForm(forms.ModelForm):
    # link = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Invite or .me Link'}))
    # accounts = forms.ModelMultipleChoiceField(
    #     queryset=Account.objects.filter(status=Account.READY),
    #     required=True
    # )

    class Meta:
        model = SampleModel
        exclude = ['owner', ]

    def __init__(self, *args, **kwargs):
        super(SampleModelForm, self).__init__(*args, **kwargs)
        # self.fields["accounts"].initial = (
        #     Account.objects.free().values_list(
        #         'id', flat=True
        #     )
        # )

    def clean(self):
        super(SampleModelForm, self).clean()
        lgr.info('clean SampleModelForm')

        # access cleaned data
        account_email = self.cleaned_data.get("email")

        valid = False

        if not valid:

            raise forms.ValidationError("Invalid Account Credentials")
        else:
            lgr.info('credentials valid')
