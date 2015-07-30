"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, url_for, redirect, request, flash, session
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

    logged_in_user = User.query.filter_by(user_id=id).first()
    
    return render_template('user_info.html', user=logged_in_user)
                        


@app.route("/login", methods=["POST", "GET"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    user_email = request.form.get("email")
    user_password = request.form.get("password")
   
    this_user = db.session.query(User.user_id).filter_by(email=user_email).first()
    
    if this_user is None:
        new_user = User(email=user_email, password=user_password)
        db.session.add(new_user)
        db.session.commit()
        this_user = db.session.query(User.user_id).filter_by(email=user_email).first()
        flash("Welcome, %s! You've created an account. Your password is %s." %(user_email, user_password))
    else:
        flash("Welcome back, %s!" %(user_email))
    
    session['user_id'] = this_user.user_id
    
    
    
    user = int(session['user_id'])
    return redirect('/users/%d' %(user))
    
@app.route("/logout")
def process_logout():
    session.pop('user_id', None)
    flash("You have successfully logged out.")
    return redirect('/')

@app.route("/movies")
def show_movies():
    """Return page showing list of all the movies.
    """
    movies = Movie.query.all()
    return render_template('movies.html', movies=movies)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    toolbar = DebugToolbarExtension(app)

    app.run()