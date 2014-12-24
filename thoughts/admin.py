from django.contrib import admin

from .models import Movie, Thought


class MovieAdmin(admin.ModelAdmin):
    pass

admin.site.register(Movie, MovieAdmin)


class ThoughtAdmin(admin.ModelAdmin):
    pass

admin.site.register(Thought, ThoughtAdmin)
