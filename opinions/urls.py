from django.conf.urls import url

from .views import OpinionView, CreateOpinionView


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', OpinionView.as_view(), name='opinion'),
    url(r'^create/$', CreateOpinionView.as_view(), name='create'),
]
