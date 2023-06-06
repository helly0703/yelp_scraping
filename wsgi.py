"""Application entry point."""

from yelp_project import create_app

app = create_app()

if __name__ == "__main__":
    app.run()  # default port is 5000, you can change port and host
