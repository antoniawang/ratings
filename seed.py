"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import User, Rating, Movie, connect_to_db, db
from server import app
import time
import datetime

def load_users():
    """Load users from u.user into database."""

    users_file = open('seed_data/u.user')

    for line in users_file:
        line = line.strip()
        user_record = line.split("|")

        new_user = User(age=user_record[2], zipcode=user_record[4])
        db.session.add(new_user)
       



def load_movies():
    """Load movies from u.item into database."""

    items_file = open('seed_data/u.item')

    for line in items_file:
        line = line.strip()
        movie_record = line.split("|")
        movie_title = movie_record[1].split(" (")
        movie_title_clean = movie_title[0].strip()
        date = movie_record[2].strip()
        if date:
            date_time = datetime.datetime.strptime(date.strip(), "%d-%b-%Y")

        

        
        new_movie = Movie(movie_id=movie_record[0], title=movie_title_clean,
            released_at=date_time, imdb_url=movie_record[3])
        db.session.add(new_movie)
    

        
def load_ratings():
    """Load ratings from u.data into database."""

    ratings_file = open('seed_data/u.data')

    for line in ratings_file:
        line = line.strip()
        rating_record = line.split("\t")

        new_rating = Rating(movie_id=rating_record[1], user_id=rating_record[0],
            score=rating_record[2])

        db.session.add(new_rating)
        



if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_movies()
    load_ratings() 
    db.session.commit()
