from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class PrivateViewMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_on_private_page'] = True
        return context
