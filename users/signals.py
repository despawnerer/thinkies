from django.dispatch import Signal


social_auth_complete = Signal(providing_args=['user', 'backend'])
