from .models import User, Identity
from .actions import update_identity as do_update_identity


# connection

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


def update_identity(user, backend, **kwargs):
    do_update_identity(user, backend.name)


# disconnection

def delete_identities(user, name, **kwargs):
    if user.default_identity and user.default_identity.provider == name:
        user.default_identity = None

    user.identities.filter(provider=name).delete()

    if user.default_identity is None:
        user.default_identity = user.identities.first()
        user.save(update_fields=['default_identity'])
