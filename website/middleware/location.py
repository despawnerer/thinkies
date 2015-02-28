from collections import namedtuple
from ipware.ip import get_real_ip

from django.conf import settings

from thinkies.geoip import locate


LOCATION_SESSION_KEY = 'location'


Location = namedtuple('Location', ('country', 'city'))


class LocationMiddleware(object):
    def process_request(self, request):
        if LOCATION_SESSION_KEY in request.session:
            location = self.get_location_from_session(request)
        else:
            location = self.get_location_from_ip(request)

        request.location = location
        self.save_location_to_session(request, location)

    def save_location_to_session(self, request, location):
        pass
        # request.session.set(LOCATION_SESSION_KEY, location)

    def get_location_from_session(self, request):
        return None

    def get_location_from_ip(self, request):
        if settings.DEBUG and getattr(settings, 'DEBUG_IP', None):
            ip = settings.DEBUG_IP
        else:
            ip = get_real_ip(request)

        if ip is None:
            return None

        result = locate(ip)
        if result is None:
            return None

        return Location(
            result.country.name,
            result.city.name)
