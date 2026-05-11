# Number Guessing Game — Senior Engineer's Build Guide

### Full-Stack Python Web Application · Phase-by-Phase with IDE Prompts

***

## 1. ARCHITECTURAL OVERVIEW

### What You're Building

A full-stack web application for a Number Guessing Game with:

- User authentication (register/login with JWT)
- Multi-difficulty gameplay (Easy / Moderate / Expert)
- Hint system, attempt limiting, and scoring
- Leaderboard and user profiles
- Admin panel for user/content management
- Feedback and Contact pages
- Encrypted passwords, token-based auth

### Recommended Stack

| Layer            | Technology                       | Why                                             |
| ---------------- | -------------------------------- | ----------------------------------------------- |
| Backend          | Python + Flask                   | Lightweight, fast to scaffold, strong ecosystem |
| Database         | SQLite (dev) → PostgreSQL (prod) | Flask-SQLAlchemy works seamlessly               |
| Auth             | Flask-JWT-Extended               | Token-based, secure, stateless                  |
| Frontend         | Jinja2 templates + TailwindCSS   | Simple, server-rendered, no build step friction |
| Password Hashing | bcrypt (via Flask-Bcrypt)        | Industry standard                               |
| Admin Panel      | Flask-Admin                      | Plug-and-play                                   |
| ORM              | SQLAlchemy                       | Clean models, migration-friendly                |
| Migrations       | Flask-Migrate (Alembic)          | Reliable schema management                      |

### High-Level Folder Structure

```
number_guessing/
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # DB models (User, Game, Score, Feedback)
│   ├── auth/
│   │   ├── routes.py        # /register, /login, /logout
│   │   └── forms.py
│   ├── game/
│   │   ├── routes.py        # /play, /guess, /result
│   │   └── logic.py         # Random number, scoring, difficulty
│   ├── leaderboard/
│   │   └── routes.py        # /leaderboard
│   ├── profile/
│   │   └── routes.py        # /profile/<username>
│   ├── admin/
│   │   └── views.py         # Flask-Admin views
│   ├── contact/
│   │   └── routes.py        # /contact
│   ├── feedback/
│   │   └── routes.py        # /feedback
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── auth/
│   │   ├── game/
│   │   ├── leaderboard/
│   │   ├── profile/
│   │   ├── contact.html
│   │   └── feedback.html
│   └── static/
│       ├── css/
│       └── js/
├── config.py
├── run.py
├── requirements.txt
└── .env
```

***

## 2. DATA MODELS (Schema Design)

```
User
  id, username (unique), email (unique), password_hash,
  is_admin, created_at

Game
  id, user_id (FK), difficulty, secret_number, max_attempts,
  attempts_used, status (active/won/lost), score, started_at, ended_at

Guess
  id, game_id (FK), guess_value, result (too_high/too_low/correct), guessed_at

Feedback
  id, user_id (FK, nullable), message, submitted_at
```

### Scoring Formula

`score = max(0, (max_attempts - attempts_used) * difficulty_multiplier * 100)`

| Difficulty | Range  | Max Attempts | Multiplier |
| ---------- | ------ | ------------ | ---------- |
| Easy       | 0–99   | 10           | 1x         |
| Moderate   | 0–999  | 10           | 2x         |
| Expert     | 0–9999 | 10           | 3x         |

***

## 3. SECURITY CHECKLIST

- [ ] Passwords hashed with bcrypt (never stored plaintext)
- [ ] JWT tokens with expiry (15min access / 7day refresh)
- [ ] CSRF protection on all forms (Flask-WTF)
- [ ] Input validation server-side (WTForms validators)
- [ ] Admin routes decorated with `@admin_required`
- [ ] `.env` used for secrets, never committed to Git
- [ ] SQL injection prevented via SQLAlchemy ORM (no raw SQL)

***

## 4. BUILD PHASES

### Phase 1 — Project Scaffold & Configuration

**Goal:** Working Flask app, DB connected, config ready, dependencies installed.
**Deliverables:** `run.py`, `config.py`, `app/__init__.py`, `requirements.txt`, `.env`

### Phase 2 — Database Models

**Goal:** All SQLAlchemy models defined and migrations working.
**Deliverables:** `models.py`, initial migration files

### Phase 3 — Authentication (Register/Login/Logout)

**Goal:** Full auth flow with bcrypt + JWT. Protected routes working.
**Deliverables:** `auth/routes.py`, `auth/forms.py`, register/login templates

### Phase 4 — Game Engine & Core Gameplay

**Goal:** Difficulty selection, random number generation, guess submission, hint feedback, attempt limiting.
**Deliverables:** `game/logic.py`, `game/routes.py`, gameplay templates

### Phase 5 — Scoring & Leaderboard

**Goal:** Score computed at game end, persisted, leaderboard rendered with rankings.
**Deliverables:** Scoring logic in `game/logic.py`, `leaderboard/routes.py`, leaderboard template

### Phase 6 — User Profile

**Goal:** Profile page showing games played, wins, best score.
**Deliverables:** `profile/routes.py`, profile template

### Phase 7 — Admin Panel

**Goal:** Admin can view/manage users, games, feedback.
**Deliverables:** `admin/views.py`, Flask-Admin registered views

### Phase 8 — Contact & Feedback Pages

**Goal:** Static contact info page, feedback form that saves to DB.
**Deliverables:** `contact/routes.py`, `feedback/routes.py`, forms and templates

### Phase 9 — Home Page & UI Polish

**Goal:** Engaging home page with game info, responsive design, TailwindCSS styling across all pages.
**Deliverables:** `home.html`, `base.html`, complete styling pass

### Phase 10 — Testing & Validation

**Goal:** Route tests, model tests, input validation edge cases covered.
**Deliverables:** `tests/` folder with pytest tests

***

## 5. CONTEXT-ENGINEERED IDE PROMPTS (Phase by Phase)

***

### PHASE 1 PROMPT — Project Scaffold

```
## Context
You are a Senior Python Engineer bootstrapping a Flask web application called "NumberGuesser" — a number guessing game with user auth, scoring, a leaderboard, and an admin panel.

## Stack
- Python 3.11+
- Flask (app factory pattern using create_app())
- Flask-SQLAlchemy (ORM)
- Flask-Migrate (Alembic migrations)
- Flask-JWT-Extended (token auth)
- Flask-Bcrypt (password hashing)
- Flask-WTF (forms + CSRF)
- Flask-Admin (admin panel)
- python-dotenv (env vars)
- SQLite for dev (config-switchable to PostgreSQL)

## Task
Scaffold the full project structure. Generate:

1. `requirements.txt` with all packages pinned to stable versions
2. `.env.example` with: SECRET_KEY, JWT_SECRET_KEY, DATABASE_URL, ADMIN_EMAIL, ADMIN_PASSWORD
3. `config.py` with DevelopmentConfig and ProductionConfig classes
4. `app/__init__.py` with a create_app() factory that initialises all extensions (db, migrate, bcrypt, jwt, csrf, admin)
5. `run.py` that calls create_app() and runs with debug=True in development

## Requirements
- Use Blueprint architecture (auth, game, leaderboard, profile, contact, feedback will each be their own Blueprint)
- Include a health check route GET /health that returns {"status": "ok"}
- Ensure JWT errors return JSON responses (not HTML)
- All config values must be loaded from environment variables via os.environ.get()

## Output Format
Produce each file clearly labelled with its path. Include inline comments explaining key decisions.
```

***

### PHASE 2 PROMPT — Database Models

```
## Context
You are continuing work on the NumberGuesser Flask app (already scaffolded with Flask-SQLAlchemy, Flask-Migrate, app factory pattern).

## Task
Create `app/models.py` with all SQLAlchemy models and run the initial migration.

## Models Required

### User
- id (Integer PK)
- username (String 80, unique, not null)
- email (String 120, unique, not null)
- password_hash (String 256, not null)
- is_admin (Boolean, default False)
- created_at (DateTime, default utcnow)
- Relationships: games (one-to-many), feedbacks (one-to-many)
- Methods: set_password(password), check_password(password) using Flask-Bcrypt

### Game
- id (Integer PK)
- user_id (FK → user.id)
- difficulty (String: 'easy'|'moderate'|'expert')
- secret_number (Integer, not null)
- max_attempts (Integer, default 10)
- attempts_used (Integer, default 0)
- status (String: 'active'|'won'|'lost', default 'active')
- score (Integer, default 0)
- started_at (DateTime, default utcnow)
- ended_at (DateTime, nullable)
- Relationship: guesses (one-to-many)

### Guess
- id (Integer PK)
- game_id (FK → game.id)
- guess_value (Integer, not null)
- result (String: 'too_high'|'too_low'|'correct')
- guessed_at (DateTime, default utcnow)

### Feedback
- id (Integer PK)
- user_id (FK → user.id, nullable — anonymous allowed)
- message (Text, not null)
- submitted_at (DateTime, default utcnow)

## Scoring Logic
Add a static method on Game: `calculate_score(difficulty, attempts_used, max_attempts)` → returns integer score.
Formula: max(0, (max_attempts - attempts_used) * multiplier * 100)
Multipliers: easy=1, moderate=2, expert=3

## Additional
- Add a __repr__ on each model
- Register all models with Flask-Admin in app/__init__.py (basic ModelView)
- Generate migration: `flask db init`, `flask db migrate -m "initial models"`, `flask db upgrade`

Produce the full models.py and the updated app/__init__.py snippet for admin registration.
```

***

### PHASE 3 PROMPT — Authentication

```
## Context
Flask app "NumberGuesser" is scaffolded with models (User, Game, Guess, Feedback) and Flask-JWT-Extended, Flask-Bcrypt, Flask-WTF installed. The auth Blueprint is registered at prefix /auth.

## Task
Implement full user authentication: Registration, Login, Logout.

## Routes to Build (all under /auth)

### POST /auth/register
- Form fields: username, email, password, confirm_password
- Validate: username/email uniqueness, password min 8 chars, passwords match
- Hash password with bcrypt, save User to DB
- Redirect to /auth/login on success with flash message

### POST /auth/login
- Form fields: username, password
- Validate credentials (username exists, password matches hash)
- Issue JWT access token (stored in httponly cookie)
- Redirect to /game/select on success

### GET /auth/logout
- Clear JWT cookie
- Redirect to home

## Files to Create
1. `app/auth/routes.py` — all route handlers
2. `app/auth/forms.py` — RegistrationForm, LoginForm using Flask-WTF
3. `app/templates/auth/register.html` — extends base.html, styled with Tailwind
4. `app/templates/auth/login.html` — extends base.html, styled with Tailwind

## Security Requirements
- Decorate protected routes with a custom @login_required decorator that checks JWT cookie
- Redirect unauthenticated users to /auth/login
- CSRF tokens included on all forms
- Flash messages for errors and success
- Never reveal whether username or email specifically caused a login failure (say "Invalid credentials")

## Helper
Create `app/auth/decorators.py` with:
- `@login_required` — verifies JWT cookie, injects current_user into g
- `@admin_required` — checks current_user.is_admin, aborts 403 if not
```

***

### PHASE 4 PROMPT — Game Engine & Gameplay

````
## Context
Flask app "NumberGuesser" has auth working. The game Blueprint is registered at /game. Models: Game, Guess are defined. Users are authenticated via JWT cookie. current_user is available via Flask's g object (set by @login_required).

## Task
Implement the full game engine and gameplay routes.

## Files to Create
1. `app/game/logic.py` — pure business logic (no Flask imports)
2. `app/game/routes.py` — route handlers
3. `app/templates/game/select.html` — difficulty selection
4. `app/templates/game/play.html` — main game UI
5. `app/templates/game/result.html` — win/lose screen

## Logic (app/game/logic.py)
```python
DIFFICULTY_CONFIG = {
    'easy':     {'min': 0, 'max': 99,   'max_attempts': 10, 'multiplier': 1},
    'moderate': {'min': 0, 'max': 999,  'max_attempts': 10, 'multiplier': 2},
    'expert':   {'min': 0, 'max': 9999, 'max_attempts': 10, 'multiplier': 3},
}

def generate_secret(difficulty: str) -> int: ...
def evaluate_guess(secret: int, guess: int) -> str:  # returns 'too_high'|'too_low'|'correct'
def calculate_score(difficulty: str, attempts_used: int, max_attempts: int) -> int: ...
def attempts_remaining(game: Game) -> int: ...
````

## Routes (app/game/routes.py)

### GET /game/select  \[@login\_required]

- Show difficulty selection page
- Show any active game warning

### POST /game/start  \[@login\_required]

- Accepts difficulty from form
- Creates new Game record (secret\_number generated, status=active)
- If user has an existing active game, end it (status=lost) first
- Redirect to /game/play

### GET /game/play  \[@login\_required]

- Load user's active game
- Render game UI with: attempt count, guess history for current game, difficulty label, range info

### POST /game/guess  \[@login\_required]

- Accepts guess (integer) from form
- Validate: must be integer, within range
- Create Guess record with result
- If correct: set game status=won, calculate+save score, redirect to /game/result
- If attempts exhausted: set status=lost, score=0, redirect to /game/result
- Else: re-render /game/play with updated hints

### GET /game/result  \[@login\_required]

- Show last completed game: outcome, score, attempts used, secret number reveal

## UI Requirements for play.html

- Show: "Attempt X of 10", current difficulty + range, guess input form
- Show history of previous guesses with ↑ Too High / ↓ Too Low indicators
- Show attempts remaining with visual indicator (e.g. progress bar)
- Disable form if game is not active

```

---
```

### PHASE 5 PROMPT — Scoring & Leaderboard

```
## Context
NumberGuesser Flask app. Game scoring logic exists in game/logic.py. Scores are saved to Game.score. The leaderboard Blueprint is registered at /leaderboard.

## Task
Build the leaderboard system.

## Routes

### GET /leaderboard  [public — no auth required]
- Query: top 20 Game records where status='won', ordered by score DESC
- Join with User to show username
- Also group by user and show their personal best score and total wins
- Render leaderboard.html

## Template (leaderboard.html)
- Styled table with: Rank, Username, Difficulty, Score, Date
- Highlight top 3 with gold/silver/bronze styling
- Show current logged-in user's row highlighted (if they appear in top 20)
- Add a filter: All / Easy / Moderate / Expert (query param ?difficulty=)

## Additional
- On the game result page, show: "You ranked #N on the leaderboard!" (query the user's rank dynamically)
```

***

### PHASE 6 PROMPT — User Profile

```
## Context
NumberGuesser Flask app. User, Game models exist. Auth is working. Profile Blueprint registered at /profile.

## Task
Build the user profile page.

## Route

### GET /profile  [@login_required]
- Aggregate stats for current user:
  - total_games: count of all games
  - total_wins: count of games where status='won'
  - win_rate: (wins/total * 100)%
  - best_score: max(score) across all won games
  - games_by_difficulty: breakdown of games per difficulty level
  - recent_games: last 10 games (date, difficulty, status, score, attempts_used)

## Template (profile.html)
- Header: username + join date
- Stats cards: Total Games, Wins, Win Rate, Best Score
- Bar chart or visual breakdown by difficulty (can use simple HTML/CSS bars, no JS library needed)
- Recent games table: clickable rows showing game details
- Link to edit profile (stub — just show a "coming soon" message)
```

***

### PHASE 7 PROMPT — Admin Panel

```
## Context
NumberGuesser Flask app. Flask-Admin is installed and initialised in create_app(). Models: User, Game, Guess, Feedback.

## Task
Build a secure, functional admin panel.

## File: app/admin/views.py

## Requirements
1. Create custom ModelView subclasses with @admin_required enforced on every admin route
2. UserAdmin view:
   - column_list: id, username, email, is_admin, created_at
   - column_searchable_list: username, email
   - column_filters: is_admin, created_at
   - Do NOT expose password_hash column
   - Add action: "Reset Password" → sets a temporary password and flashes it

3. GameAdmin view:
   - column_list: id, username (via relationship), difficulty, status, score, attempts_used, started_at
   - column_filters: difficulty, status
   - Read-only (no edit/delete to preserve game integrity)

4. FeedbackAdmin view:
   - column_list: id, username (nullable), message, submitted_at
   - Allow delete (admin can remove inappropriate feedback)

5. Register an admin-only dashboard index view at /admin/ showing:
   - Total users, Total games played today, Total wins today, Total feedback count

## Security
- All admin views must override is_accessible() to check current_user.is_admin
- Override inaccessible_callback() to redirect to /auth/login with a flash("Admin access required")
- Create a CLI command: `flask create-admin` that creates the first admin user using ADMIN_EMAIL and ADMIN_PASSWORD from .env
```

***

### PHASE 8 PROMPT — Contact & Feedback

```
## Context
NumberGuesser Flask app. User model exists. Auth required. Feedback is always linked to the logged-in user.

## Task
Build Contact and Feedback pages.

## Contact Page
### GET /contact
- Static page displaying:
  - Company name: "Aptech Learning"
  - Email: support@aptech.com (placeholder)
  - Address: (placeholder address)
  - Phone: (placeholder number)
  - Styled with an icon for each contact type

## Feedback Page
### GET /feedback — render form
### POST /feedback — save to DB
- Decorate route with @login_required
- Always set Feedback.user_id = current_user.id
- Remove the nullable user_id logic entirely

## This also means you can make user_id non-nullable in the Feedback model, which is cleaner schema design. If you've already run the migration with it nullable, add a quick migration to tighten that constraint:
 ```bash
flask db migrate -m "make feedback user_id non-nullable"
flask db upgrade

## File: app/feedback/routes.py, app/feedback/forms.py
## Templates: contact.html, feedback.html (both extend base.html)
```

***

### PHASE 9 PROMPT — Home Page & UI Polish

```
## Context
NumberGuesser Flask app — all routes and logic are complete. Now build a polished, engaging UI.

## Task
Create the home page and apply a consistent design system across all templates.

## base.html Requirements
- TailwindCSS via CDN
- Navbar: Logo/brand, links (Home, Play, Leaderboard, Contact, Feedback), Login/Register or Username + Logout
- Flash message display (dismissible alerts, colour-coded: success=green, error=red, info=blue)
- Footer: copyright, links

## Home Page (home.html)
- Hero section: Large headline "Can You Guess the Number?", subtext, "Play Now" CTA button
- How to Play section: 3-step visual (Choose Difficulty → Enter Guess → Win or Lose)
- Difficulty cards: Easy / Moderate / Expert — show range and description
- Leaderboard preview: top 5 players shown on home
- Screenshots or placeholder images for visual engagement

## Design Direction
- Color palette: Deep navy (#0F172A) background, electric cyan accent (#06B6D4), white text
- Game-like feel: monospace font for numbers, clean sans-serif for body
- Smooth transitions on hover states
- Responsive: mobile-first, hamburger menu on small screens

## Polish Pass (apply to ALL templates)
- Consistent card styling, consistent button styles (primary/secondary/danger)
- Form error states: red border + error message below field
- Loading state on guess submit button (disable + "Checking..." text via JS)
- Animate guess history rows sliding in
- Active nav link highlighted
```

***

### PHASE 10 PROMPT — Testing & Validation

```
## Context
NumberGuesser Flask app — fully built. Now add tests.

## Stack
- pytest
- pytest-flask (app fixture)
- Factory Boy or direct model creation for test data

## Task
Create a `tests/` folder with the following test files:

### tests/conftest.py
- App fixture with TESTING=True, in-memory SQLite
- Client fixture
- Authenticated client fixture (logs in a test user, stores JWT cookie)
- Admin client fixture

### tests/test_auth.py
- test_register_success
- test_register_duplicate_username
- test_register_password_mismatch
- test_login_success
- test_login_wrong_password
- test_logout

### tests/test_game.py
- test_start_game_easy
- test_start_game_creates_secret_in_range
- test_guess_too_low
- test_guess_too_high
- test_guess_correct_sets_won
- test_guess_correct_calculates_score
- test_max_attempts_reached_sets_lost
- test_guess_out_of_range_rejected
- test_guess_non_integer_rejected

### tests/test_leaderboard.py
- test_leaderboard_shows_top_players
- test_leaderboard_filter_by_difficulty

### tests/test_admin.py
- test_non_admin_cannot_access_admin
- test_admin_can_access_admin

## Coverage Target
Aim for >80% coverage. Run: `pytest --cov=app tests/`
```

***

## 6. QUICK REFERENCE — Environment Setup Commands

```bash
# Create virtual environment
python -m venv venv && source venv/bin/activate  # Linux/Mac
python -m venv venv && venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# (Edit .env with your values)

# Initialize database
flask db init
flask db migrate -m "initial"
flask db upgrade

# Create first admin user
flask create-admin

# Run development server
flask run

# Run tests
pytest --cov=app tests/ -v
```

***

## 7. DEPLOYMENT NOTES (When Ready)

- Switch `DATABASE_URL` to PostgreSQL connection string
- Set `FLASK_ENV=production` in environment
- Use Gunicorn: `gunicorn -w 4 run:app`
- Serve static files via Nginx or WhiteNoise
- Use HTTPS — JWT cookies must have `secure=True` in production
- Set `JWT_COOKIE_SECURE=True` and `SESSION_COOKIE_SECURE=True` in config

***

*Guide generated for the Aptech NumberGuesser eProject · Python/Flask · 10-Phase Build*
