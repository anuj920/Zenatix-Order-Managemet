from django.core.exceptions import PermissionDenied

def user_is_superuser(function):
    def wrap(self, request, *args, **kwargs):
        if request.user and request.user.is_superuser:
            return function(self, request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap