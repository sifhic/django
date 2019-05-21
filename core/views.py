from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from core.forms import SampleModelForm

from django.conf import settings

import logging

import json

# Create your views here.
lgr = logging.getLogger(__name__)


def dashboard(request):
    return render(request, 'core/dashboard.html', {})


from core.forms import SampleModelForm


def sample_create(request):
    if request.method == "POST":
        lgr.info(request.POST)
        form = SampleModelForm(request.POST)
        if form.is_valid():
            search = form.save(commit=False)
            search.account = request.user
            search.save()

            form.save_m2m()

            titles = request.POST.getlist('titles[]')
            for title in titles:
                # new instance created
                search.title.add(title_instance)

            lgr.info('saved search')

            sample_task.delay(search.pk)

            return redirect('/')
        else:
            lgr.error('search form error')
            lgr.error(form.errors)

    else:
        form = SampleModelForm()

    return render(request, "core/search/create.html", {
        'form': form,
    })
