from django.conf.urls import include, url


urlpatterns = [
    url(r'^auth/logout/', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^auth/', include(
        'social.apps.django_app.urls', namespace='social')),

    url(r'^movies/', include('movies.urls', namespace='movies')),
]
