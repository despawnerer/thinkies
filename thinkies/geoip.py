import os
from geoip2.errors import AddressNotFoundError
from geoip2.database import Reader

from django.conf import settings


def locate(ip_address):
    reader = Reader(os.path.join(settings.GEOIP_PATH, settings.GEOIP_CITY))
    try:
        return reader.city(ip_address)
    except AddressNotFoundError:
        return None
