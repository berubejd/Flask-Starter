from flask import Blueprint, current_app as app, redirect, render_template, url_for

from . import create_app
from . import db
from .models import Test


main_bp = Blueprint(
    "routes", __name__, template_folder="templates", static_folder="static"
)


@main_bp.route("/", methods=["GET"])
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
