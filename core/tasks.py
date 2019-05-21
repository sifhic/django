from __future__ import absolute_import, unicode_literals
from celery import shared_task

import logging

lgr = logging.getLogger(__name__)


@shared_task
def sample_task():
    pass


