from urllib.parse import urlsplit, parse_qs


def first(iterable):
    for x in iterable:
        return x
    else:
        return None


def get_param_from_url(url, param):
    query_string = urlsplit(url).query
    params = parse_qs(query_string)
    return params.get(param)[0]
