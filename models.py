from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model. A user can login and logout. A user can update their own info, but not another user's"""

    __tablename__ = 'users'

    username = db.Column(db.String, nullable=False,
                         unique=True, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)

    feedback = db.relationship(
        "Feedback", backref="user", cascade="all,delete")

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user with hashed password & return user"""
        hashed = bcrypt.generate_password_hash(pwd)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.
        Reutn user if valid; else return False"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False


class Feedback(db.Model):
    """Feedback model. Users can give feedback on the most amazing app ever built. Not that it needs it..."""

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String,
        db.ForeignKey('users.username'),
        nullable=False)
