from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_bcrypt import Bcrypt
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from sqlalchemy.orm.collections import attribute_mapped_collection


db = SQLAlchemy()
bcrypt = Bcrypt()


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.LargeBinary, nullable=True)
    roles = db.relationship("Role", secondary="user_roles")

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    @password.deleter
    def password(self):
        self.password_hash = None

    @property
    def has_password(self):
        return bool(self.password_hash)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def has_role(self, tested_role):
        return (
            True
            if [role for role in self.roles if role.name.lower() == tested_role.lower()]
            else False
        )

    def add_role(self, add_role):
        if not self.has_role(add_role):
            role = db.session.query(Role).filter_by(name=add_role).first()
            if role:
                found_role = UserRoles(user_id=self.id, role_id=role.id)
                db.session.add(found_role)
                db.session.commit()
            else:
                return False
        return True

    def delete_role(self, del_role):
        if self.has_role(del_role):
            role = db.session.query(Role).filter_by(name=del_role).first()
            if role:
                found_role = UserRoles(user_id=self.id, role_id=role.id)
                db.session.delete(found_role)
                db.session.commit()
            else:
                return False
        return True

    def __repr__(self):
        return self.username


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return self.name


class UserRoles(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))


class OAuth(OAuthConsumerMixin, db.Model):
    __table_args__ = (db.UniqueConstraint("provider", "provider_user_id"),)
    provider_user_id = db.Column(db.String(256), nullable=False)
    provider_user_login = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(
        User,
        # This `backref` thing sets up an `oauth` property on the User model,
        # which is a dictionary of OAuth models associated with that user,
        # where the dictionary key is the OAuth provider name.
        backref=db.backref(
            "oauth",
            collection_class=attribute_mapped_collection("provider"),
            cascade="all, delete-orphan",
        ),
    )


# Setup login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Seed functions
role_list = [
    "admin",
]


def seed_roles(roles=role_list):
    updates = False

    for role in roles:
        existing_role = Role.query.filter_by(name=role).first()

        if not existing_role:
            updates = True

            new_role = Role(name=role)
            db.session.add(new_role)

    if updates:
        db.session.commit()
