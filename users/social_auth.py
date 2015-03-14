from .models import User, Identity
from .signals import social_auth_complete


def create_user(strategy, details, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    email = details.get('email')
    user = User.objects.create_user(email=email)
    return {'is_new': True, 'user': user}


def create_identity(user, backend, details, uid, **kwargs):
    identity, created = Identity.objects.update_or_create(
        user=user, provider=backend.name, defaults={
            'uid': uid,
            'name': details.get('fullname', '')[:255],
        })

    if user.default_identity is None:
        user.default_identity = identity
        user.save(update_fields=['default_identity'])

    return {'identity': identity}


def send_signal(user, backend, **kwargs):
    social_auth_complete.send(
        sender=user.__class__, user=user, backend=backend)
