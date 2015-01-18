from django.conf.urls import url

from .views import TipView, TipListView, CreateTipView


urlpatterns = [
    url(r'^$', TipListView.as_view(), name='tip_list'),
    url(r'^(?P<pk>\d+)/$', TipView.as_view(), name='tip'),
    url(r'^create/$', CreateTipView.as_view(), name='create'),
]
