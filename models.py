"""Models for adopt app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)

# my users will have a username, first name, last name and email

class User(db.Model):

    __tablename__ = "users"

    username = db.Column(db.Text, primary_key=True)
    email = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    

class Todo(db.Model):

    __tablename__ = "todos"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    task = db.Column(db.Text, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    todo_username = db.Column(db.Text, db.ForeignKey("users.username"))

    # if I make a db.relationship in 1 table
        # but I want to reference both tables....?
            # backref

    user = db.relationship("User", backref="todos")
