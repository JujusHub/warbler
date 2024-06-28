from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

class Likes(db.Model):
    """Mapping user likes to warbles."""
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id', ondelete='cascade'), unique=True)

class User(db.Model):
    """User in the system."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(db.Text, default="/static/images/default-pic.png")
    header_image_url = db.Column(db.Text, default="/static/images/warbler-hero.jpg")
    bio = db.Column(db.Text)
    location = db.Column(db.Text)
    password = db.Column(db.Text, nullable=False)

    messages = db.relationship('Message')
    followers = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_being_followed_id == id),
        secondaryjoin=(Follows.user_following_id == id)
    )
    following = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_following_id == id),
        secondaryjoin=(Follows.user_being_followed_id == id)
    )
    likes = db.relationship('Message', secondary='likes')
