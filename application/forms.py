from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Length
from sqlalchemy.exc import IntegrityError
from .models import db, User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")

    def get_user(self):
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            # Set error on password field to obfuscate reason for login failure
            self.password.errors.append("Incorrect username or password")
            return None
        if not user.verify_password(self.password.data):
            self.password.errors.append("Incorrect username or password")
            return None
        return user


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("repeat_password", message="Passwords must match"),
        ],
    )
    repeat_password = PasswordField("Repeat Password")
    submit = SubmitField("Register")

    def create_user(self):
        user = User(username=self.username.data)
        user.password = self.password.data
        db.session.add(user)
        try:
            db.session.commit()
            return user
        except IntegrityError:
            self.username.errors.append("This username is already in use")
            return None


class SetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("repeat_password", message="Passwords must match"),
        ],
    )
    repeat_password = PasswordField("Repeat Password")
    submit = SubmitField("Set Password")


class ContactForm(FlaskForm):
    name = TextField(
        "Name",
        validators=[
            DataRequired("Please enter your name."),
            Length(min=4, message="Please enter at least 4 chars"),
        ],
    )
    email = TextField(
        "Email",
        validators=[
            DataRequired("Please enter your email address."),
            Email("Please enter a valid email address."),
        ],
    )
    subject = TextField("Subject",
        validators=[
            DataRequired("Please enter a subject."),
            Length(min=8, message="Please enter at least 8 chars for the subject"),
        ],
    )
    message = TextAreaField(
        "Message", validators=[DataRequired("Please write something for us")]
    )
    submit = SubmitField("Send")
