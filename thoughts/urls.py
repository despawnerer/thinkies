from django.conf.urls import include, url
from django.contrib import admin

from .views import Index

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^auth/logout/', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^auth/', include(
        'social.apps.django_app.urls', namespace='social')),

    url(r'^$', Index.as_view()),
]
