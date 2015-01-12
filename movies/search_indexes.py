from haystack import indexes

from thinkies.search.fields import CharField

from .models import Movie


class MovieIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='title')
    imdb_id = indexes.CharField(model_attr='imdb_id')
    year = indexes.IntegerField(model_attr='year')
    title_en = CharField(analyzer='english')
    title_ru = CharField(analyzer='russian')
    title_fr = CharField(analyzer='french')
    title_es = CharField(analyzer='spanish')
    title_de = CharField(analyzer='german')
    title_nl = CharField(analyzer='dutch')
    title_sv = CharField(analyzer='swedish')
    title_hi = CharField(analyzer='hindi')
    title_no = CharField(analyzer='norwegian')
    title_nb = CharField(analyzer='norwegian')
    title_nn = CharField(analyzer='norwegian')
    title_pt = CharField(analyzer='portuguese')
    title_it = CharField(analyzer='italian')
    title_da = CharField(analyzer='danish')

    def get_model(self):
        return Movie

    def index_queryset(self, using=None):
        return self.get_model().objects.prefetch_related('title_translations')

    def prepare_title_en(self, obj):
        return obj.titles_by_language.get('en') or ''

    def prepare_title_ru(self, obj):
        return obj.titles_by_language.get('ru') or ''

    def prepare_title_fr(self, obj):
        return obj.titles_by_language.get('fr') or ''

    def prepare_title_es(self, obj):
        return obj.titles_by_language.get('es') or ''

    def prepare_title_de(self, obj):
        return obj.titles_by_language.get('de') or ''

    def prepare_title_nl(self, obj):
        return obj.titles_by_language.get('nl') or ''

    def prepare_title_sv(self, obj):
        return obj.titles_by_language.get('sv') or ''

    def prepare_title_hi(self, obj):
        return obj.titles_by_language.get('hi') or ''

    def prepare_title_no(self, obj):
        return obj.titles_by_language.get('no') or ''

    def prepare_title_nb(self, obj):
        return obj.titles_by_language.get('nb') or ''

    def prepare_title_nn(self, obj):
        return obj.titles_by_language.get('nn') or ''

    def prepare_title_pt(self, obj):
        return obj.titles_by_language.get('pt') or ''

    def prepare_title_it(self, obj):
        return obj.titles_by_language.get('it') or ''

    def prepare_title_da(self, obj):
        return obj.titles_by_language.get('da') or ''
