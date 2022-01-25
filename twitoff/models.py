from flask_sqlalchemy import SQLAlchemy


# Create a DB object
DB = SQLAlchemy()


# Create a table with a specific schema
# We will do that by creating a python class that
# inherits from SQLAlchemy Model class

class User(DB.Model):
    # Two columns inside of our user table
    # ID column schema (id is an integer, however big,
    # will be the primary key and cannot be null)
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)

    # username column schema (user is a string and
    # cannot be null)
    username = DB.Column(DB.String, nullable=False)

    # Tweets list is created by the .relationship and backref
    # in the Tweets class


class Tweet(DB.Model):

    # ID column schema
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)

    # Text column schema
    text = DB.Column(DB.Unicode(300), nullable=False)

    # User column schema
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)

    # Set up a relationship between the tweets and the user
    # This will automatically create the one-to-many relationship,
    # but also add a new attribute onto the "user" class called
    # "tweets" which will be a lsit of all the user tweets
    user = DB.relationship("User", backref=DB.backref('tweets'), lazy=True)
