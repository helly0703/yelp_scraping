"""Application entry point."""
from flask_migrate import Migrate

from yelp_project import create_app, db

app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":

    app.run()  # default port is 5000, you can change port and host
