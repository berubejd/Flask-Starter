from flask import Blueprint, current_app as app, render_template
from ..models import db, Test


blueprint = Blueprint(
    "routes", __name__, template_folder="templates", static_folder="static"
)


@blueprint.route("/", methods=["GET"])
def index():
    heading = "Welcome!"
    message = "Hello, world!"

    existing_test_row = Test.query.filter(Test.first == "DB Test").first()

    if not existing_test_row:
        new_test_row = Test(first="DB Test")

        db.session.add(new_test_row)
        db.session.commit()

    else:
        print(f"Found test row at id: {existing_test_row.id}")

    return render_template("index.html", heading=heading, message=message)


@blueprint.route("/features", methods=["GET"])
def features():
    pass


@blueprint.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")
