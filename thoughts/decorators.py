from functools import wraps

from django.views.generic.base import View
from django.http import HttpResponseBadRequest
from django.core.exceptions import ImproperlyConfigured


def view_decorator(decorator):
    """
    Helper decorator that simplifies writing decorators that work
    on both class-based views and function views.

    Example:

    @view_decorator
    def print_kwargs(f, request, *args, **kwargs):
        print("KWARGS:")
        for key, value in kwargs.iteritems():
            print("{}: {}".format(key, value))
        return f(request, *args, **kwargs)

    @print_kwargs
    class MyView(View):
        pass

    @print_kwargs
    def my_view(request, **kwargs):
        return None
    """
    @wraps(decorator)
    def decorator_wrapper(decoratee):
        if isinstance(decoratee, type):
            if not issubclass(decoratee, View):
                raise ImproperlyConfigured(
                    "\"%s\" decorator can only be used on view functions or"
                    " classes extending View" % decorator.__name__)

            def dispatch(self, *args, **kwargs):
                super_dispatch = super(decoratee, self).dispatch
                return decorator(super_dispatch, *args, **kwargs)
            return type(
                decoratee.__name__,
                (decoratee,),
                {'dispatch': dispatch})
        else:
            @wraps(decoratee)
            def wrapper(*args, **kwargs):
                return decorator(decoratee, *args, **kwargs)
            return wrapper
    return decorator_wrapper


@view_decorator
def ajax_only(f, request, *args, **kwargs):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    else:
        return f(request, *args, **kwargs)
