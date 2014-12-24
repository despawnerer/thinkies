from django.conf.urls import include, url
from django.contrib import admin

from .views import Index

urlpatterns = [
    url(r'^$', Index.as_view()),

    url(r'^admin/', include(admin.site.urls)),
]
