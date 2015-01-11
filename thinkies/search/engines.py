from haystack.backends.elasticsearch_backend import (
    ElasticsearchSearchEngine,
    ElasticsearchSearchBackend,
)


class ConfigurableElasticBackend(ElasticsearchSearchBackend):
    def build_schema(self, fields):
        content_field_name, mapping = (
            super(ConfigurableElasticBackend, self).build_schema(fields))
        for field_name, field in fields.items():
            analyzer = getattr(field, 'analyzer', None)
            if analyzer:
                mapping[field_name]['analyzer'] = analyzer
        return content_field_name, mapping


class ConfigurableElasticEngine(ElasticsearchSearchEngine):
    backend = ConfigurableElasticBackend
