from django.conf.urls import url,include
from core.views import (
    dashboard,

)

app_name = 'core'

urlpatterns = [

    url(r'^$', dashboard, name='dashboard'),

    # url(r'^ta', core_ta, name='ta'),

    # url(r'^sample_model/', include(([
    #     url(r'^create$', search_create,name='create'),
    #
    #     url(r'^(?P<sample_model_pk>\d+)/', include(([
    #         url(r'^$', search_summary, name='summary'),
    #         url(r'^track_node$', search_track_node, name='track_node'),
    #
    #     ],'search'))),
    # ],'searches'))),
]
