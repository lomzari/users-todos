"""Flask app for adopt app."""
from flask import Flask, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Todo

app = Flask(__name__)

app.config['SECRET_KEY'] = "abcdef"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///users_todos"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route("/")
def home():
    return redirect("/users")

@app.route("/users")
def show_users():
    all_users = User.query.all()
    return render_template("users_index.html", users=all_users)

@app.route("/users/<username>")
def show_user(username):
    found_user = User.query.get_or_404(username)
    return render_template("user_show.html", user=found_user)
