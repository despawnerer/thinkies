from .actions import update_friends


def update_friends_on_auth(user, backend, **kwargs):
    update_friends(user, backend.name)
