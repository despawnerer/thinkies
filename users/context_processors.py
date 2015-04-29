from .actions import get_auth_providers


def auth_providers(request):
    return {'auth_providers': get_auth_providers(request.user)}
