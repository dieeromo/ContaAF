
from functools import wraps
from django.http import HttpResponseForbidden



def custom_permission_required(allowed_roles=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("Acceso denegado. Debes estar autenticado.")
            
            if allowed_roles and not any(role in allowed_roles for role in user.groups.values_list('name', flat=True)):
                return HttpResponseForbidden("Acceso denegado. No tienes los roles necesarios.")
            
            return view_func(request, *args, **kwargs)
        
        return _wrapped_view
    return decorator