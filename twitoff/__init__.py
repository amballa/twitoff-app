from .app import create_app

# This step makes sure our app is always created before
# anything else happens and we don't have to export the
# app on the command line
APP = create_app()
