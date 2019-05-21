from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from authentication.models import User
# Create your models here.

import os
import logging
from django.conf import settings

lgr = logging.getLogger(__name__)


def file_cleanup(sender, instance, using, **kwargs):
    settings_path = instance.session_file_path()

    if os.path.exists(settings_path):
        os.remove(settings_path)


from django.db.models.signals import post_delete


class SampleModel(models.Model):

    class Meta:
        managed = False

# post_delete.connect(file_cleanup, sender=SalesNavigatorAccount)

