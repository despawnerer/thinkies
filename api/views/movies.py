from rest_framework import viewsets, serializers

from movies.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'translated_title', 'year', 'mpaa_rating',
                  'release_date', 'poster', 'imdb_id', 'imdb_rating',
                  'imdb_votes')


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
