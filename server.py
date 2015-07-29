"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.config['SECRET_KEY'] = '<replace with a secret key>'
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/users/<int:id>")
def show_user(id):
    """Return page showing the details of a given user.
    """
    logged_in_user = User.query.filter_by(user_id=id).one()
    print logged_in_user


    return render_template('user_info.html', user=logged_in_user)
                        


@app.route("/login", methods=["POST"])
def process_login(id):
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    user_id = request.form.get("id")
    print user_id
    new_email = request.form.get("email")
    new_password = request.form.get("password")
    session['user_id'] = user_id
    
    flash("You are now logged in!")
    user = session['user_id']

    return redirect('/users/<int:id>', id=user_id)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    toolbar = DebugToolbarExtension(app)

    app.run()