from flask import Blueprint, request, redirect, url_for, flash, render_template, session
from flask_login import login_required, login_user, logout_user, current_user
from application.models import db, User, OAuth
from application.forms import RegisterForm, LoginForm, SetPasswordForm


blueprint = Blueprint("auth", __name__, template_folder="templates")


@blueprint.route("/profile")
@login_required
def profile():
    return render_template("profile.j2")


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = form.create_user()
        if user:
            login_user(user)
            flash("Account created")
            return redirect(url_for("main.index"))
    return render_template("register.j2", form=form)


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    session["next_url"] = request.args.get("next")
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user()
        if user:
            login_user(user)
            flash("You have logged in")
            return redirect(url_for("main.index"))
    return render_template("login.j2", form=form)


@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("main.index"))


@blueprint.route("/password", methods=["GET", "POST"])
@login_required
def password():
    form = SetPasswordForm()
    if form.validate_on_submit():
        current_user.password = form.password.data
        db.session.add(current_user)
        db.session.commit()
        flash("Password set successfully")
        return redirect(url_for("auth.profile"))
    return render_template("password.j2", form=form)


@blueprint.route("/merge", methods=["GET", "POST"])
@login_required
def merge():
    form = LoginForm(data={"username": request.args.get("username")})
    if form.validate_on_submit():
        user = form.get_user()
        if user:
            if user != current_user:
                merge_users(current_user, user)
                flash(f"User { user.username } has been merged into your account")
                return redirect(url_for("main.index"))
            else:
                form.username.errors.append("Cannot merge with yourself")
    return render_template("merge.j2", form=form)


def merge_users(merge_into, merge_from):
    assert merge_into != merge_from
    OAuth.query.filter_by(user=merge_from).update({"user_id": merge_into.id})
    db.session.delete(merge_from)
    db.session.commit()
    return merge_into


@blueprint.route("/unlink/<provider>")
@login_required
def unlink(provider):
    oauth_link = OAuth.query.filter_by(
        user_id=current_user.id, provider=provider
    ).first()
    if oauth_link:
        db.session.delete(oauth_link)
        db.session.commit()
        flash(f"{ provider.title() } has been unlinked from your account")
    else:
        flash(f"No account link for { provider } found", "warning")
    return redirect(url_for("auth.profile"))
