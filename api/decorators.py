from functools import wraps

from django_www.utils import resp_err, resp_success
from api.db_manager import get_setting

def api_check_maintenance(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        is_mt = get_setting().get('is_maintenance')
        if is_mt is True:
            return resp_err('System maintenance')
        return f(request, *args, **kwargs)

    return wrapper