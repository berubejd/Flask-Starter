from flask import Blueprint, current_app as app, render_template, session, redirect, flash, url_for
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ..forms import ContactForm

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


@blueprint.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        message = Mail(
            from_email=form.email.data,
            to_emails=app.config['CONTACT_EMAIL'],
            subject=form.subject.data,
            html_content=form.message.data)

        try:
            sg = SendGridAPIClient(app.config['SENDGRID_API_KEY'])
            response = sg.send(message)
            flash("Your message has been sent. Thank you!")

        except Exception as e:
            flash("Something went wrong.  Please try again later.")
            print(e.message)

        return redirect(url_for("main.contact"))
        
    return render_template("contact.j2", form=form)
