from functools import wraps
import functools
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page

# def cache_on_auth(timeout):
#     def decorator(view_func):
#         @wraps(view_func, assigned=functools.WRAPPER_ASSIGNMENTS)
#         def _wrapped_view(request, *args, **kwargs):
#             return cache_page(timeout, key_prefix="_auth_%s_" % request.user.is_authenticated())(view_func)(request, *args, **kwargs)
#         return _wrapped_view
#     return decorator


def unauthenticated_user(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('taskList')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_function
