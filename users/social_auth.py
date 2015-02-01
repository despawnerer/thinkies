from .signals import social_auth_complete


def send_signal(user, backend, **kwargs):
    social_auth_complete.send(
        sender=user.__class__, user=user, backend=backend)
