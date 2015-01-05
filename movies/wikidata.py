import ijson.backends.yajl2 as ijson
import dateutil.parser
from funcy import cached_property, notnone


def load_items(f):
    for json in ijson.items(f, 'item'):
        yield Item(json)


class Item:
    def __init__(self, json):
        self.json = json

    @cached_property
    def type(self):
        return self.json.get('type')

    @cached_property
    def id(self):
        return self.json.get('id')

    @cached_property
    def labels(self):
        label_jsons = self.json.get('labels')
        return {
            language: json['value']
            for language, json in label_jsons.items()}

    @cached_property
    def properties(self):
        statement_jsons = self.json.get('claims') or {}
        return ItemProperties(statement_jsons)


class ItemProperties:
    def __init__(self, statement_jsons_by_property):
        self.json = statement_jsons_by_property
        self._keys = self.json.keys()
        self._values = {}

    def __contains__(self, key):
        return key in self._keys

    def __getitem__(self, key):
        if key not in self._keys:
            raise KeyError
        elif key in self._values:
            return self._values[key]
        else:
            json_list = self.json[key]
            all_values = map(self._get_value_from_statement_json, json_list)
            actual_values = list(filter(notnone, all_values))
            self._values[key] = actual_values
            return self._values[key]

    def _get_value_from_statement_json(self, json):
        mainsnak = json['mainsnak']
        if 'datavalue' not in mainsnak:
            return None

        datavalue = mainsnak['datavalue']
        type_ = datavalue['type']
        value = datavalue['value']

        if type_ == 'time':
            date_string = value['time']
            # cut off the first character 'cause it's a sign
            first_dash_index = date_string[1:].index('-')
            year = int(date_string[:first_dash_index])
            if 0 < year < 9999:
                # only leave the 4-digit year so we can parse this
                date_string = date_string[first_dash_index-4:]
                value = dateutil.parser.parse(date_string)
            else:
                # we can't convert BCE dates and dates past year 9999 so
                # we leave those as strings
                value = date_string

        return value
