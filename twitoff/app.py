from flask import Flask, render_template
from .models import DB, User, Tweet
from os import getenv
from .twitter import add_or_update_user

# "Factory" - a function for setting up our app


def create_app():

    app = Flask(__name__)

    # Configuration variable to our app
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Connect our databse to the app object
    DB.init_app(app)

    @app.route("/")
    def home_page():
        # query for all users in the database
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/populate')
    # Test my database functionality
    # by inserting some fake data into the DB
    def populate():
        # Reset the databse first
        # Remove everything from the DB
        # DB.drop_all()
        # Recreate the user and Tweet tables so that
        # they're ready to used (inserted into)
        # DB.create_all()

        add_or_update_user('ryanallred')
        add_or_update_user('nasa')
        add_or_update_user('joerogan')

        # Make two test users
        # elon = User(id=1, username='elonmusk')
        # joe = User(id=2, username='joerogan')

        # # Make six test tweets and attaching the tweets to two users
        # tweet1 = Tweet(id=1, text="This is annoying", user=elon)
        # tweet2 = Tweet(
        #     id=2, text="Twitter is spending engineering resources on this bs while crypto scammers are throwing a spambot block party in every thread!?""", user=elon)
        # tweet3 = Tweet(
        #     id=3, text="Tesla AI might play a role in AGI, given that it trains against the outside world, especially with the advent of Optimus", user=elon)
        # tweet4 = Tweet(id=4, text="Believe in the future!", user=elon)
        # tweet5 = Tweet(
        #     id=5, text="We need to talk about the vaccines - UnHerd", user=joe)
        # tweet6 = Tweet(
        #     id=6, text="10 rounds in the books. Didn't want to do it. Did it anyway.", user=joe)

        # # Inserting into the DB when working with SQLite directly
        # DB.session.add(elon)
        # DB.session.add(joe)
        # DB.session.add(tweet1)
        # DB.session.add(tweet2)
        # DB.session.add(tweet3)
        # DB.session.add(tweet4)
        # DB.session.add(tweet5)
        # DB.session.add(tweet6)

        # Commit the DB changes
        # DB.session.commit()

        return render_template('base.html', title='Populate')

    @app.route('/update')
    # Update existing users
    def update():
        usernames = get_usernames()
        for username in usernames:
            add_or_update_user(username)

        return render_template('base.html', title='Update User Tweets')

    @app.route('/reset')
    def reset():
        # Do some database stuff
        # Drop old DB tables
        # Remake new DB tables
        # Remove everything from the DB
        DB.drop_all()
        # Recreate the user and Tweet tables so that
        # they're ready to used (inserted into)
        DB.create_all()
        return render_template('base.html', title='Reset Database')

    return app


def get_usernames():
    # first get all of the usernames of existing users
    Users = User.query.all()
    usernames = []
    for user in Users:
        usernames.append(user.username)
    return usernames
