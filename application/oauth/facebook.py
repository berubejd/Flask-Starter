from flask import flash, url_for, redirect
from flask_login import current_user, login_user
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from application.models import db, User, OAuth


blueprint = make_facebook_blueprint(
    scope="email", storage=SQLAlchemyStorage(OAuth, db.session, user=current_user)
)


# create/login local user on successful OAuth login
@oauth_authorized.connect_via(blueprint)
def facebook_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with Facebook.", category="error")
        return False

    resp = blueprint.session.get("/me?fields=id,name,picture,email")
    if not resp.ok:
        msg = "Failed to fetch user info from Facebook."
        flash(msg, category="error")
        return False

    facebook_info = resp.json()
    print(facebook_info)
    """ Response:

        default:
        {
            'name': 'First Last', 
            'id': '123456789'
        }

        current:
        {
            'id': '123456789', 
            'name': 'First Last', 
            'picture': {
                'data': {
                    'height': 50, 
                    'is_silhouette': False, 
                    'url': 'https://platform-lookaside.fbsbx.com/platform/profilepic/?asid=123456789&height=50&width=50&ext=1584611310&hash=ABCABCABC_ABC', 
                    'width': 50
                }
            }
        }
    """
    facebook_user_id = facebook_info["id"]

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name, provider_user_id=facebook_user_id
    )
    try:
        oauth = query.one()
    except NoResultFound:
        facebook_user_login = str(facebook_info["name"])
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=facebook_user_id,
            provider_user_login=facebook_user_login,
            token=token,
        )

    # Now, figure out what to do with this token. There are 2x2 options:
    # user login state and token link state.

    if current_user.is_anonymous:
        if oauth.user:
            login_user(oauth.user)
            flash("Successfully signed in with Facebook.")

        else:
            # Create a new local user account for this user
            user = User(username=facebook_info["name"])
            # Associate the new local user account with the OAuth token
            oauth.user = user
            # Save and commit our database models
            db.session.add_all([user, oauth])
            db.session.commit()
            # Log in the new local user account
            login_user(user)
            flash("Successfully signed in with Facebook.")
    else:
        if oauth.user:
            # If the user is logged in and the token is linked, check if these
            # accounts are the same!
            if current_user != oauth.user:
                # Account collision! Ask user if they want to merge accounts.
                url = url_for("auth.merge", username=oauth.user.username)
                return redirect(url)
        else:
            # If the user is logged in and the token is unlinked,
            # link the token to the current user
            oauth.user = current_user
            db.session.add(oauth)
            db.session.commit()
            flash("Successfully linked Facebook account.")

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False


# notify on OAuth provider error
@oauth_error.connect_via(blueprint)
def facebook_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")
