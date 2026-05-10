import os

from dotenv import load_dotenv

from app import create_app

load_dotenv()

# The app object is exposed at module scope so `flask run` and WSGI servers can import it.
app = create_app()


if __name__ == "__main__":
    is_development = os.environ.get("FLASK_ENV", "development") == "development"
    app.run(debug=is_development)
