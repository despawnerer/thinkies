from .actions import update_identity


def update_identity_on_auth(user, backend, **kwargs):
    update_identity(user, backend.name)
