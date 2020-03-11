from flask import current_app, flash, redirect, request, url_for
from flask_login import current_user
from functools import wraps
from urllib.parse import urlparse, urljoin


def role_required(
    role,
    target="main.index",
    msg="You don't have the required permissions to view that page.",
):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            if not current_user.has_role(role):
                flash(msg)
                return redirect(url_for(target))
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


def is_safe_url(target):
    """
    A function that ensures that a redirect target will lead to the same server
    A common pattern with form processing is to automatically redirect back to
    the user. There are usually two ways this is done: by inspecting a next URL
    parameter or by looking at the HTTP referrer. Unfortunately you also have to
    make sure that users are not redirected to malicious attacker's pages and
    just to the same host.
    Source: http://flask.pocoo.org/snippets/62/ (No longer hosted by the project)
    Archive: https://web.archive.org/web/20190128005233/http://flask.pocoo.org/snippets/62
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc
