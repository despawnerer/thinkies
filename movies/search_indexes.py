from haystack import indexes

from thoughts.search.fields import CharField

from .models import Movie, TitleTranslation


class MovieIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='title')
    imdb_id = indexes.CharField(model_attr='imdb_id')
    year = indexes.IntegerField(model_attr='year')
    title_en = CharField(analyzer='english')
    title_ru = CharField(analyzer='russian')

    def get_model(self):
        return Movie

    def index_queryset(self, using=None):
        return self.get_model().objects.prefetch_related('title_translations')

    def prepare_title_en(self, obj):
        return self._get_title_translation(obj, 'en')

    def prepare_title_ru(self, obj):
        return self._get_title_translation(obj, 'ru')

    def _get_title_translation(self, obj, language):
        translations = obj.title_translations.all()
        for trans in translations:
            if trans.language == language:
                return trans.title
        else:
            return ''
