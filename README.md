# NumberGuesser

`Python 3.11+` `Flask` `MIT License` `PRs Welcome`

A production-aware Flask number guessing game with JWT cookie authentication, score tracking, a public leaderboard, user profiles, feedback flow, and an admin panel.

## Table of Contents
- [About the Project](#about-the-project)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Environment Variables Reference](#environment-variables-reference)
- [Scoring System](#scoring-system)
- [Security Notes](#security-notes)
- [Contributing](#contributing)
- [License](#license)

## About the Project
NumberGuesser is a server-rendered Flask web application built around a classic number guessing game with a more complete product experience layered on top. Players can register, log in, choose a difficulty, make guesses with hint feedback, and compete for better scores on a global leaderboard. The application uses Flask Blueprints and the app factory pattern so each feature area stays modular and maintainable as the project grows.

The project is designed to demonstrate practical full-stack Flask architecture rather than only game logic. It includes secure authentication with JWT tokens stored in HTTP-only cookies, SQLAlchemy models and migrations, profile statistics, feedback capture, and a restricted admin interface for platform management. PostgreSQL is the primary database for development and production, while SQLite remains an option for quick local experimentation or tests.

The frontend uses Jinja2 templates and TailwindCSS via CDN, which keeps deployment simple because Flask serves both the application logic and the HTML views. There is no separate JavaScript build pipeline, frontend framework, or client-side dev server required to run the application.

### Features
- User registration and login with JWT cookie authentication and bcrypt password hashing
- Three difficulty levels: Easy (`0-99`), Moderate (`0-999`), Expert (`0-9999`)
- Hint feedback after each guess: `Too High`, `Too Low`, or correct result
- Ten attempts per game with score calculation based on difficulty and attempts used
- Public leaderboard showing the top 20 winning games, with difficulty filtering
- User profile page with totals, wins, win rate, best score, difficulty breakdown, and recent games
- Admin panel for managing users, reviewing game records, and moderating feedback
- Contact and feedback pages for user communication and product input
- Input validation, CSRF protection, and environment-based configuration throughout

## Tech Stack
| Layer | Technology | Purpose |
|---|---|---|
| Backend | Python 3.11+, Flask, Flask Blueprints | Application logic, routing, and modular structure |
| Database | PostgreSQL, SQLite | Persistent storage for users, games, guesses, and feedback |
| ORM | Flask-SQLAlchemy, SQLAlchemy, Flask-Migrate, Alembic | Data models, queries, and schema migrations |
| Auth | Flask-JWT-Extended, Flask-Bcrypt | JWT cookie auth and password hashing |
| Forms | Flask-WTF, WTForms | Form rendering, CSRF protection, and validation |
| Frontend | Jinja2, TailwindCSS via CDN | Server-rendered HTML templates and styling |
| Admin | Flask-Admin | Restricted admin dashboard and model management |
| Testing | pytest, pytest-flask, pytest-cov | Route tests, validation checks, and coverage reporting |

## Project Structure
```text
NumberGuesser/                          # Project root
├── app/                                # Main application package
│   ├── __init__.py                     # App factory, extension setup, core routes, blueprint registration
│   ├── models.py                       # SQLAlchemy models for users, games, guesses, and feedback
│   ├── auth/                           # Authentication blueprint
│   │   ├── __init__.py                 # Auth blueprint export
│   │   ├── decorators.py               # Login and admin access decorators
│   │   ├── forms.py                    # Registration and login WTForms classes
│   │   └── routes.py                   # Register, login, and logout routes
│   ├── game/                           # Gameplay blueprint
│   │   ├── __init__.py                 # Game blueprint export
│   │   ├── logic.py                    # Pure gameplay logic and scoring helpers
│   │   └── routes.py                   # Difficulty selection, active game, guessing, and result routes
│   ├── leaderboard/                    # Leaderboard blueprint
│   │   ├── __init__.py                 # Leaderboard blueprint export
│   │   └── routes.py                   # Public rankings and leaderboard filters
│   ├── profile/                        # User profile blueprint
│   │   ├── __init__.py                 # Profile blueprint export
│   │   └── routes.py                   # Player statistics and recent game history
│   ├── admin/                          # Admin integration package
│   │   ├── __init__.py                 # Admin exports
│   │   └── views.py                    # Secure Flask-Admin views and CLI bootstrap command
│   ├── contact/                        # Contact blueprint
│   │   ├── __init__.py                 # Contact blueprint export
│   │   └── routes.py                   # Static contact page route
│   ├── feedback/                       # Feedback blueprint
│   │   ├── __init__.py                 # Feedback blueprint export
│   │   ├── forms.py                    # Feedback submission form
│   │   └── routes.py                   # Authenticated feedback routes
│   ├── templates/                      # Jinja2 templates used by Flask views
│   │   ├── admin/                      # Admin dashboard template
│   │   ├── auth/                       # Login and registration templates
│   │   ├── game/                       # Difficulty selection, play, and result templates
│   │   ├── leaderboard/                # Leaderboard template
│   │   ├── profile/                    # Profile template
│   │   ├── base.html                   # Shared layout, navigation, flashes, and footer
│   │   ├── contact.html                # Public contact page
│   │   ├── feedback.html               # Feedback submission page
│   │   └── home.html                   # Landing page
│   └── static/                         # Optional location for custom static assets if added later
├── migrations/                         # Alembic migration environment and version history
│   └── versions/                       # Generated migration scripts
├── tests/                              # Pytest suite and shared fixtures
├── venv/                               # Local virtual environment (created during setup, not committed)
├── config.py                           # Environment-driven config classes
├── run.py                              # App entry point for `python run.py` and `flask run`
├── requirements.txt                    # Pinned Python dependencies
├── .env.example                        # Example environment variable file
├── .env                                # Local secrets and runtime config (create locally, never commit)
└── README.md                           # Project documentation
```

## Prerequisites
Install the following before setting up the project:

- Python `3.11+`
- PostgreSQL `14+`
- Git

PostgreSQL installation notes:

- Ubuntu/Debian: `sudo apt update && sudo apt install postgresql postgresql-contrib`
- macOS with Homebrew: `brew install postgresql@14`
- Windows: install PostgreSQL using the official graphical installer from the PostgreSQL website and ensure `psql` is added to your `PATH`

Verify each dependency is available:

```bash
python --version
psql --version
git --version
```

## Getting Started
### 7.1 Clone the Repository
```bash
git clone https://github.com/yourusername/numberguesser.git
cd numberguesser
```

### 7.2 Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
venv\Scripts\activate
```

### 7.3 Install Dependencies
```bash
pip install -r requirements.txt
```

### 7.4 Set Up Environment Variables
Create a local `.env` file in the project root using the following values as a starting point:

```dotenv
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
DATABASE_URL=postgresql://numberguesser_user:yourpassword@localhost:5432/numberguesser_db
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=change-me-before-production
```

Generate secure values for `SECRET_KEY` and `JWT_SECRET_KEY`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

> Never commit your `.env` file. Store secrets locally or inject them through your deployment environment.

### 7.5 Set Up PostgreSQL Database
Start the PostgreSQL shell:

```bash
sudo -u postgres psql
```

Then run:

```sql
CREATE USER numberguesser_user WITH PASSWORD 'yourpassword';
CREATE DATABASE numberguesser_db OWNER numberguesser_user;
GRANT ALL PRIVILEGES ON DATABASE numberguesser_db TO numberguesser_user;
\q
```

### 7.6 Run Database Migrations
Set the Flask app entry point if needed, then apply migrations:

```bash
export FLASK_APP=run.py
# PowerShell:
$env:FLASK_APP="run.py"
flask db upgrade
```

### 7.7 Create the Admin User
```bash
flask create-admin
```

## Running the Application
This is a server-rendered Flask application, so there is no separate frontend server, Node.js build step, or client bundle process. Flask handles the application logic and renders the Jinja2 templates directly on each request.

Start the app with either command:

```bash
flask run
# or
python run.py
```

Default local URL:

```text
http://127.0.0.1:5000
```

Jinja2 templates are rendered by Flask on the server, which means visiting a route in the browser is enough to use the interface. There is no `npm run dev`, no separate SPA process, and no extra frontend runtime to manage.

| Route | Access | Description |
|---|---|---|
| `/` | Public | Home page |
| `/auth/register` | Public | Create an account |
| `/auth/login` | Public | Log in |
| `/game/select` | Auth required | Choose difficulty |
| `/game/play` | Auth required | Active game |
| `/leaderboard` | Public | Top players |
| `/profile` | Auth required | Your stats |
| `/feedback` | Auth required | Submit feedback |
| `/contact` | Public | Contact info |
| `/admin/` | Admin only | Admin panel |

## Running Tests
Run the full test suite with coverage:

```bash
pytest --cov=app tests/ -v
```

The test suite covers authentication flows, gameplay state transitions, leaderboard rendering, protected admin access, and key route behaviors such as feedback and profile pages.

Example output format:

```text
============================= test session starts =============================
collected 26 items

tests/test_admin.py ..                                                   [  7%]
tests/test_auth.py ......                                                [ 30%]
tests/test_game.py .........                                             [ 65%]
tests/test_leaderboard.py ..                                             [ 73%]
tests/test_pages.py .......                                              [100%]

=============================== tests coverage ================================
TOTAL                                                                  84%
============================= 26 passed in 22s ===============================
```

## Environment Variables Reference
| Variable | Required | Description | Example |
|---|---|---|---|
| `SECRET_KEY` | Yes | Flask secret key used for session and form security features | `f3d7...` |
| `JWT_SECRET_KEY` | Yes | Signing key for JWT tokens | `0c91...` |
| `DATABASE_URL` | Yes | SQLAlchemy database connection string | `postgresql://numberguesser_user:yourpassword@localhost:5432/numberguesser_db` |
| `ADMIN_EMAIL` | Yes | Email used by `flask create-admin` | `admin@example.com` |
| `ADMIN_PASSWORD` | Yes | Password used by `flask create-admin` | `change-me-before-production` |
| `FLASK_ENV` | No | Chooses `development` or `production` config | `development` |
| `FLASK_DEBUG` | No | Enables Flask debug mode in development | `true` |
| `JWT_ACCESS_TOKEN_MINUTES` | No | Access token lifetime in minutes | `15` |
| `JWT_REFRESH_TOKEN_DAYS` | No | Refresh token lifetime in days | `7` |
| `JWT_COOKIE_CSRF_PROTECT` | No | Enables JWT cookie CSRF enforcement if needed | `false` |
| `JWT_COOKIE_SECURE` | No | Marks JWT cookies as HTTPS-only | `true` |

## Scoring System
Score is computed when a game is won using the formula:

```text
score = (max_attempts - attempts_used) x multiplier x 100
```

That means faster wins on harder difficulties produce higher scores.

| Difficulty | Range | Multiplier | Max Attempts |
|---|---|---|---|
| Easy | `0-99` | `1x` | `10` |
| Moderate | `0-999` | `2x` | `10` |
| Expert | `0-9999` | `3x` | `10` |

Example:

```text
Moderate win in 4 attempts = (10 - 4) x 2 x 100 = 1200
```

## Security Notes
- Passwords are hashed with `Flask-Bcrypt`; plain-text passwords are never stored
- Authentication uses JWTs stored in HTTP-only cookies
- Forms use `Flask-WTF` with CSRF protection
- Routes validate user input before writing to the database
- SQLAlchemy ORM is used instead of raw SQL queries in application code
- Secrets are loaded from environment variables and should live in `.env` or deployment config

## Contributing
Contributions are welcome.

Standard workflow:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests locally
5. Open a pull request

Branch naming convention:

```text
feature/your-feature-name
```

## License
This project is licensed under the MIT License.

```text
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
