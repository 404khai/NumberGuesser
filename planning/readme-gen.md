## Context
You are a Senior Technical Writer and Software Engineer documenting the "NumberGuesser" Flask web application for a GitHub repository README. The project is complete and production-aware.

## Project Summary (for accuracy — do not invent details outside this)
- **App:** Number Guessing Game web application
- **Backend:** Python 3.11+, Flask, Flask-Blueprints, Flask-SQLAlchemy, Flask-Migrate, Flask-JWT-Extended, Flask-Bcrypt, Flask-WTF, Flask-Admin
- **Database:** PostgreSQL (production/dev), SQLite optional for quick local runs
- **Frontend:** Jinja2 server-rendered HTML templates, TailwindCSS via CDN
- **Auth:** JWT stored in HTTP-only cookies, bcrypt password hashing
- **Structure:** App factory pattern (create_app()), modular Blueprints (auth, game, leaderboard, profile, admin, contact, feedback)
- **Testing:** pytest + pytest-flask + pytest-cov
- **Virtual Environment:** venv

## Task
Generate a complete, professional GitHub README.md for this project.

## Required Sections (in this order)

### 1. Header
- Project name as H1
- A one-sentence tagline
- Badges (static markdown badges, no external services needed):
  - Python version (3.11+)
  - Flask
  - License: MIT
  - PRs Welcome

### 2. Table of Contents
- Linked to every major section below

### 3. About the Project
- 2-3 paragraph overview of what the app does and why it exists
- Feature list (use a clean bullet list):
  - User registration and login (JWT + bcrypt)
  - Three difficulty levels: Easy (0–99), Moderate (0–999), Expert (0–9999)
  - Hint system (Too High / Too Low) with 10 attempts per game
  - Scoring system based on difficulty and attempts used
  - Leaderboard (top 20 players, filterable by difficulty)
  - User profile with stats (games played, wins, win rate, best score)
  - Admin panel (user management, game logs, feedback review)
  - Feedback and Contact pages
  - Input validation and CSRF protection throughout

### 4. Tech Stack
- Formatted table: Layer | Technology | Purpose
- Rows: Backend, Database, ORM, Auth, Forms, Frontend, Admin, Testing

### 5. Project Structure
- Full annotated folder tree matching this structure:
NumberGuesser/
├── app/
│   ├── init.py
│   ├── models.py
│   ├── auth/
│   ├── game/
│   ├── leaderboard/
│   ├── profile/
│   ├── admin/
│   ├── contact/
│   ├── feedback/
│   ├── templates/
│   └── static/
├── migrations/
├── tests/
├── venv/
├── config.py
├── run.py
├── requirements.txt
└── .env

- Add a brief inline comment (using #) next to each key file/folder explaining its role

### 6. Prerequisites
- List what must be installed before setup:
  - Python 3.11+
  - PostgreSQL 14+ (with install note for Ubuntu, macOS Homebrew, Windows)
  - Git
- Include the exact commands to verify each is installed:
```bash
  python --version
  psql --version
  git --version
```

### 7. Getting Started (Setup)
Break this into clearly numbered sub-steps:

**7.1 Clone the Repository**
```bash
git clone https://github.com/yourusername/numberguesser.git
cd numberguesser
```

**7.2 Create and Activate Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

**7.3 Install Dependencies**
```bash
pip install -r requirements.txt
```

**7.4 Set Up Environment Variables**
- Show the full .env.example contents:
```dotenv
  SECRET_KEY=your-secret-key-here
  JWT_SECRET_KEY=your-jwt-secret-here
  DATABASE_URL=postgresql://numberguesser_user:yourpassword@localhost:5432/numberguesser_db
  ADMIN_EMAIL=admin@example.com
  ADMIN_PASSWORD=change-me-before-production
```
- Include the two commands to generate secure keys:
```bash
  python -c "import secrets; print(secrets.token_hex(32))"  # Run twice — once per key
```

**7.5 Set Up PostgreSQL Database**
```bash
sudo -u postgres psql

# Inside psql:
CREATE USER numberguesser_user WITH PASSWORD 'yourpassword';
CREATE DATABASE numberguesser_db OWNER numberguesser_user;
GRANT ALL PRIVILEGES ON DATABASE numberguesser_db TO numberguesser_user;
\q
```

**7.6 Run Database Migrations**
```bash
flask db upgrade
```

**7.7 Create the Admin User**
```bash
flask create-admin
```

### 8. Running the Application
- Explain that this is a server-rendered app — there is no separate frontend server or build step
- Show:
```bash
  flask run
  # or
  python run.py
```
- State default URL: http://127.0.0.1:5000
- Explain how Jinja2 templates work in one short paragraph: Flask serves both the logic and the HTML — visiting any route in the browser is all that is needed; there is no npm run dev or separate client process
- Add a route reference table:

  | Route | Access | Description |
  |---|---|---|
  | / | Public | Home page |
  | /auth/register | Public | Create an account |
  | /auth/login | Public | Log in |
  | /game/select | Auth required | Choose difficulty |
  | /game/play | Auth required | Active game |
  | /leaderboard | Public | Top players |
  | /profile | Auth required | Your stats |
  | /feedback | Auth required | Submit feedback |
  | /contact | Public | Contact info |
  | /admin/ | Admin only | Admin panel |

### 9. Running Tests
```bash
pytest --cov=app tests/ -v
```
- Explain what is tested (auth, game logic, leaderboard, admin access)
- Show example expected output format

### 10. Environment Variables Reference
- Full table: Variable | Required | Description | Example

### 11. Scoring System
- Explain the formula: score = (max_attempts - attempts_used) × multiplier × 100
- Table showing difficulty multipliers and ranges

### 12. Security Notes
- Short bullet list covering: bcrypt hashing, JWT in HTTP-only cookies, CSRF protection, input validation, no raw SQL, .env for secrets

### 13. Contributing
- Standard fork → branch → PR flow
- Branch naming convention: feature/your-feature-name

### 14. License
- MIT License block

## Tone and Style Rules
- Professional but readable — this is a developer-facing document, not marketing copy
- Every code block must have a language specifier (```bash, ```python, ```dotenv, ```sql)
- No placeholder waffle — if a section has nothing meaningful to say, omit it rather than pad it
- Use > blockquotes for important warnings (e.g. "Never commit your .env file")
- The README should be complete enough that a developer who has never seen this project can clone and run it with zero external help

## Output
Produce the entire README.md as a single markdown code block, ready to save as README.md in the project root.