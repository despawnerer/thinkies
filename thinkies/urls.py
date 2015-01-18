from django.conf.urls import include, url


urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^auth/logout/', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^auth/', include(
        'social.apps.django_app.urls', namespace='social')),

    url(r'^movies/', include('movies.urls', namespace='movies')),
    url(r'^tips/', include('tips.urls', namespace='tips'))
]
