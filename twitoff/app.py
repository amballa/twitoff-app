from flask import Flask, render_template, request
from .models import DB, User, Tweet
from os import getenv
from .twitter import add_or_update_user
from .predict import predict_user

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
        return render_template('base.html', title='Home', users=User.query.all())

    # @app.route('/populate')
    # # Populating DB
    # def populate():
    #     # Reset the databse first
    #     # Remove everything from the DB
    #     # DB.drop_all()
    #     # Recreate the user and Tweet tables so that
    #     # they're ready to used (inserted into)
    #     # DB.create_all()

    #     # Hard coding some example users
    #     add_or_update_user('elonmusk')
    #     add_or_update_user('joerogan')

    #     # Make two test users
    #     # elon = User(id=1, username='elonmusk')
    #     # joe = User(id=2, username='joerogan')

    #     # # Make six test tweets and attaching the tweets to two users
    #     # tweet1 = Tweet(id=1, text="This is annoying", user=elon)
    #     # tweet2 = Tweet(
    #     #     id=2, text="Twitter is spending engineering resources on this bs while crypto scammers are throwing a spambot block party in every thread!?""", user=elon)
    #     # tweet3 = Tweet(
    #     #     id=3, text="Tesla AI might play a role in AGI, given that it trains against the outside world, especially with the advent of Optimus", user=elon)
    #     # tweet4 = Tweet(id=4, text="Believe in the future!", user=elon)
    #     # tweet5 = Tweet(
    #     #     id=5, text="We need to talk about the vaccines - UnHerd", user=joe)
    #     # tweet6 = Tweet(
    #     #     id=6, text="10 rounds in the books. Didn't want to do it. Did it anyway.", user=joe)

    #     # # Inserting into the DB when working with SQLite directly
    #     # DB.session.add(elon)
    #     # DB.session.add(joe)
    #     # DB.session.add(tweet1)
    #     # DB.session.add(tweet2)
    #     # DB.session.add(tweet3)
    #     # DB.session.add(tweet4)
    #     # DB.session.add(tweet5)
    #     # DB.session.add(tweet6)

    #     # Commit the DB changes
    #     # DB.session.commit()

    #     return render_template('base.html', title='Populate')

    @app.route('/update')
    # Update existing users
    def update():
        usernames = get_usernames()
        for username in usernames:
            add_or_update_user(username)

        return render_template('base.html', title='All users have been updated')

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

    # User route is a more traditional API endpoint
    # This endpoint can only accept certain kinds of http request
    # This is the route for creating a user
    @app.route('/user', methods=['POST'])
    # This is the route for viewing a user
    @app.route('/user/<username>', methods=['GET'])
    def user(username=None, message=''):
        username = username or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(username)
                message = f"User {username} successfully added!"
            tweets = User.query.filter(User.username == username).one().tweets
        except Exception as e:
            message = f"Error adding {username}: {e}"
            tweets = []

        return render_template('user.html', title=username, tweets=tweets, message=message)

    # Our compare route
    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted(
            [request.values['user0'], request.values['user1']])

        if user0 == user1:
            message = "Cannot compare a user to themselves"
        else:
            prediction = predict_user(
                user0, user1, request.values['tweet_text'])
            message = "'{}' is more likely to be said by {} than {}!".format(request.values['tweet_text'],
                                                                             user1 if prediction else user0,
                                                                             user0 if prediction else user1)

        return render_template('prediction.html', title="Prediction", message=message)

    return app


def get_usernames():
    # first get all of the usernames of existing users
    Users = User.query.all()
    usernames = []
    for user in Users:
        usernames.append(user.username)
    return usernames
