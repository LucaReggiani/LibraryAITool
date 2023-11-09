import pandas as pd
from config import configuration
from routes import setup_routes
from models import BookModel

if __name__ == '__main__':

    app = configuration.get_app()
    api = configuration.get_api()
    db = configuration.get_db()

    # Setup the routes
    setup_routes(api)

    # getting alembic for continuous db integration
    alembic = configuration.get_alembic()

    with app.app_context():

        # creation all the tables defined in the database models
        db.create_all()

        # generate a new revision
        alembic.revision("Changes Detected!")

        # run all available upgrades
        alembic.upgrade()
        
    app.run(debug=True)