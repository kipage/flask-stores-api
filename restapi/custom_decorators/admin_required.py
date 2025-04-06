from functools import wraps
from flask_smorest import abort
from flask_jwt_extended import get_jwt


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        claims = get_jwt()["role"]
        if not "admin" in claims:
            abort(403, message="You do not have permission to perform this operation.")
        return func(*args, **kwargs)
    return wrapper