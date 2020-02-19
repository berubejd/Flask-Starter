from flask import Blueprint, current_app as app, render_template, session, redirect


blueprint = Blueprint("main", __name__)


@blueprint.route("/", methods=["GET"])
def index():
    heading = "Welcome!"
    message = "Hello, world!"

    if session.get("next_url"):
        next_url = session.get("next_url")
        session.pop("next_url", None)
        return redirect(next_url)

    return render_template("index.j2", heading=heading, message=message)


@blueprint.route("/features", methods=["GET"])
def features():
    pass


@blueprint.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.j2")
