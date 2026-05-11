## Context
You are a Senior Frontend Engineer and UI/UX Designer revamping the homepage of "NumberGuesser" — a Flask/Jinja2 number guessing game web app. You are editing `app/templates/home.html` which extends `app/templates/base.html`. TailwindCSS is loaded via CDN. All assets are in `app/images/`.

## Design System (NON-NEGOTIABLE — apply exactly)
- **Background:** #FFECD6 (warm peach — used as page and section background)
- **Primary/Brand color:** #FFCC79 (golden yellow — used for logo text, nav links, accents, active states, CTA buttons)
- **Heading Font:** "DynaPuff" (Google Fonts) — used for ALL headings, hero text, section titles, card titles
- **Body/UI Font:** "Comfortaa" (Google Fonts) — used for all body text, nav links, labels, paragraphs
- **Import both fonts via a single Google Fonts <link> tag:**
  `https://fonts.googleapis.com/css2?family=Comfortaa:wght@400;600;700&family=DynaPuff:wght@400;500;600;700&display=swap`
- **Logo:** Use `<img src="{{ url_for('static', filename='images/logo.png') }}">` — do NOT use text as logo, place image inline in navbar
- **Medal images:**
  - Gold: `{{ url_for('static', filename='images/goldMedal.png') }}`
  - Silver: `{{ url_for('static', filename='images/silverMedal.png') }}`
  - Bronze: `{{ url_for('static', filename='images/bronzeMedal.png') }}`
  - 4th place and beyond: use a plain styled number badge, no medal image

## Task
Rewrite `home.html` as a complete, production-ready Jinja2 template with beautiful, playful, polished UI. Every section below must be implemented exactly as specified.

---

## Section 1 — Navbar (Full Width)
- Full-width, sticky top, background #FFECD6 with a subtle bottom border (1px solid rgba(255,204,121,0.4))
- Left: logo.jpeg image (height 40px) — wrapped in a link to /
- Center: nav links — Home, Leaderboard, Contact — font Comfortaa, color #FFCC79, hover underline animation (CSS, not Tailwind)
- Right: if user logged in → show "Hi, username" + Logout button | if not → Login + Register buttons
- Buttons: rounded-full, background #FFCC79, text dark (#3d2c00), font Comfortaa font-semibold, hover slightly darken
- Mobile: hamburger menu that toggles links, implemented in vanilla JS — no Alpine, no jQuery
- Navbar height: compact — max 64px

---

## Section 2 — Hero Section (Full Width, Center-Aligned)
- Full-width section, centered content, padding top 96px bottom 80px, background #FFECD6
- Main headline: "Can You Guess the Number?" — DynaPuff font, large (clamp(2.5rem, 6vw, 4.5rem)), color #3d2c00 (dark brown)
- Subheadline: "Pick a difficulty, make your guesses, beat the leaderboard." — Comfortaa, 1.2rem, color #7a5c30 (muted brown)
- CTA button: "Start Playing →" — large, rounded-full, background #FFCC79, dark text, DynaPuff font, subtle bounce animation on hover (CSS keyframe)
- If user is not logged in: show secondary link below CTA "New here? Create a free account" in small Comfortaa text, color #FFCC79
- Add a fun decorative element: floating emoji-style numbers (1? 7? 3?) scattered behind the headline text using CSS absolute positioning, low opacity (0.08), DynaPuff font, very large size — purely decorative

## Section 3 — Game Levels (Full Width)
- Background: slightly warmer variant — use #FFF3E6 to create visual separation from adjacent sections
- Section title: "Choose Your Challenge" — DynaPuff, centered, color #3d2c00
- Section subtitle: "3 levels. 10 attempts each. Higher difficulty = bigger score multiplier." — Comfortaa, centered, muted color
- Display exactly 3 level cards in a horizontal row:

  **Easy**
  - Range: 0 – 99
  - Multiplier: 1× 
  - Tagline: "Perfect for warming up"
  - Accent color: #86efac (soft green)

  **Moderate**
  - Range: 0 – 999
  - Multiplier: 2×
  - Tagline: "Getting interesting…"
  - Accent color: #fcd34d (amber)

  **Expert**
  - Range: 0 – 9999
  - Multiplier: 3×
  - Tagline: "Not for the faint-hearted"
  - Accent color: #fca5a5 (soft red)

- Each card: white background, rounded-3xl, top colored accent bar (8px, using card's accent color), DynaPuff for name and range, Comfortaa for tagline, multiplier shown as a large badge
- Hover: card lifts slightly (transform translateY -4px, transition 200ms)
- Cards equal width, centered row, max-width 960px, centered in section

---

## Section 4 — How to Play (Full Width, Bento Grid Layout)
- Background: #FFECD6
- Section title: "How to Play" — DynaPuff, centered above the bento grid
- Bento grid: 2 columns — LEFT column splits into TOP and BOTTOM cards (each 50% height of the right card) — RIGHT column is one full-height card
- Total bento width: 80% of viewport, centered, rounded-3xl cards with white background and soft shadow

  **Left Top Card — Step 1: Choose Your Difficulty**
  - Icon: 🎯
  - Heading: DynaPuff
  - Body: "Pick Easy, Moderate, or Expert. The harder the level, the higher the score multiplier." — Comfortaa

  **Left Bottom Card — Step 2: Make Your Guess**
  - Icon: 🔢
  - Heading: DynaPuff  
  - Body: "Enter a number within the range. You get 10 attempts — use them wisely." — Comfortaa

  **Right Card — Step 3: Read the Hints**
  - Text at the TOP of the card:
    - Icon: 💡
    - Heading: "Read the Hints" — DynaPuff
    - Body: "After each guess, we'll tell you if the answer is higher or lower. Close in and claim the win." — Comfortaa
  - Bottom half of right card: reserved blank space for an image — use:
    `<img src="{{ url_for('static', filename='images/gameplay_preview.png') }}" alt="Gameplay preview" class="...">`
    styled to fill the bottom half, object-fit cover, rounded-xl. If image doesn't exist it should fail gracefully (no broken layout — use a soft placeholder div with background #FFF3E6 and centered text "[ Game Preview ]" in muted Comfortaa)

- Grid uses CSS Grid (not Tailwind grid) for the bento layout so the left-column split is precise:
```css
  .bento-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 1.5rem;
  }
  .bento-left-top    { grid-column: 1; grid-row: 1; }
  .bento-left-bottom { grid-column: 1; grid-row: 2; }
  .bento-right       { grid-column: 2; grid-row: 1 / span 2; }
```

---

## Section 5 — Leaderboard Preview (Full Width)
- Background: #FFF3E6
- Section title: "Leaderboard" — DynaPuff, centered, large
- Section subtitle: "The best of the best. Updated in real time." — Comfortaa, centered, muted
- Full-width table (max-width 900px, centered):
  - Columns: Rank | Player | Difficulty | Score
  - Rank column: medal image for top 3 (goldMedal, silverMedal, bronzeMedal), plain number for rest
  - Use `leaderboard_preview` passed from Flask (list of top 5, same object shape as top_scores)
  - Row styling: alternating subtle background (#FFECD6 and white), Comfortaa font, DynaPuff for score numbers
  - Top 3 rows slightly bolder, gold/silver/bronze left border accent (4px solid)
- Below the table, centered: a single CTA button "View Full Leaderboard →"
  - Style: rounded-full, background #FFCC79, dark text, DynaPuff font, same hover as hero CTA
  - Links to /leaderboard

---

## Section 6 — Footer (Full Width)
- Background: #3d2c00 (dark brown — strong contrast to page)
- Two-column layout: left = logo.png (height 32px) + tagline in Comfortaa small, white text | right = nav links (Home, Leaderboard, Contact, Feedback) in Comfortaa, color #FFCC79
- Bottom bar: centered copyright line "© 2025 NumberGuesser · Built with Flask" — Comfortaa, small, muted white

---

## Flask Route Context (what the template receives)
The home route must pass these to the template. Add this note for the developer implementing the route:
```python
# In app/home/routes.py or wherever / is handled:
from app.models import Game, User

top_scores = (
    Game.query
    .filter_by(status='won')
    .order_by(Game.score.desc())
    .limit(4)
    .all()
)

leaderboard_preview = (
    Game.query
    .filter_by(status='won')
    .order_by(Game.score.desc())
    .limit(5)
    .all()
)

return render_template('home.html',
    top_scores=top_scores,
    leaderboard_preview=leaderboard_preview,
    current_user=current_user  # from Flask's g or your auth decorator
)
```

---

## Technical Rules
- The file is a Jinja2 template — use `{% extends "base.html" %}` and `{% block content %}...{% endblock %}`
- Do NOT use Tailwind for layout-critical grid structures (bento, navbar flex) — use scoped `<style>` blocks with CSS custom properties for those
- DO use Tailwind utility classes for spacing, typography scale, border-radius, shadows, and colors where it doesn't conflict with custom layout CSS
- All custom CSS goes inside a `{% block styles %}` block at the top of the file (or inline `<style>` in the block)
- All custom JS goes inside a `{% block scripts %}` block at the bottom (hamburger menu toggle only)
- Jinja2 conditionals for auth state: use `{% if current_user %}` pattern consistent with however auth is implemented in base.html
- Image tags must use `url_for('static', filename='...')` — never hardcoded paths
- All sections must be responsive:
  - Navbar: hamburger on mobile
  - Top Scores: 2×2 grid on mobile, 4-column on desktop
  - Level cards: stack vertically on mobile
  - Bento grid: stack to single column on mobile (all 3 cards full width, stacked)
  - Leaderboard table: horizontally scrollable on mobile

## Navbar as Reusable Partial
- Extract the navbar HTML into its own file: `app/templates/partials/navbar.html`
- In base.html, include it via: `{% include 'partials/navbar.html' %}`
- Do NOT include the navbar in home.html directly — it comes through base.html
- The partial has full access to template context (current_user, request.path for active link detection) without any extra passing
- Use `request.path` to highlight the active nav link:
  `class="{{ 'active' if request.path == '/' else '' }}"`
- The hamburger JS should be scoped inside navbar.html in a <script> tag at the bottom of that file

## Output
Produce the complete `home.html` file. No placeholders, no TODOs, no stubs. Every section fully implemented, styled, and ready to render.


---- PHASE 2 - UI CONSISTENCY ---

## Context
You are a Senior Frontend Engineer completing the UI revamp of "NumberGuesser" — a Flask/Jinja2 number guessing game. The homepage has already been built and establishes the full design system. You are now applying that same design system consistently across all remaining templates. Every template extends `app/templates/base.html` which already includes the navbar partial and loads both Google Fonts.

## Design System (Carry Over Exactly — No Deviations)
- **Background:** #FFECD6
- **Primary/Brand:** #FFCC79
- **Dark text / headings:** #000000
- **Muted body text:** #7a5c30
- **Section alternate background:** #FFF3E6
- **Heading Font:** DynaPuff (all H1, H2, H3, card titles, large labels)
- **Body Font:** Comfortaa (all body text, labels, inputs, nav, buttons)
- **Border radius language:** rounded-3xl for cards, rounded-full for buttons and pills, rounded-xl for inputs and inner elements
- **Card style:** white background, rounded-3xl, soft box-shadow (0 4px 24px rgba(61,44,0,0.07)), padding 2rem
- **Primary button:** background #FFCC79, color #3d2c00, DynaPuff font, rounded-full, px-8 py-3, hover darken to #f5bc60
- **Secondary button:** transparent background, border 2px solid #FFCC79, color #3d2c00, same shape as primary, hover fill #FFCC79
- **Danger button:** background #fca5a5, color #7f1d1d, same shape
- **Input fields:** background white, border 1.5px solid #FFCC79, rounded-xl, Comfortaa font, padding 0.75rem 1rem, focus ring color #FFCC79, placeholder color #c4a882
- **Flash messages:** rounded-2xl, Comfortaa, success=#d1fae5 (green tint), error=#fee2e2 (red tint), info=#fef9c3 (yellow tint) — shown below navbar, above page content
- **Difficulty badge pills:** Easy=bg #bbf7d0 text #166534, Moderate=bg #fde68a text #92400e, Expert=bg #fecaca text #991b1b — Comfortaa font-semibold text-sm rounded-full px-3 py-1

---

## base.html Requirements
Update base.html to:
- Load Google Fonts: Comfortaa + DynaPuff via single <link> tag
- Set `font-family: 'Comfortaa', cursive` as global body font via <style>
- Set page background to #FFECD6 globally on <body>
- Include flash message block directly below `{% include 'partials/navbar.html' %}`:
```html
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      <div class="flash-container">
        {% for category, message in messages %}
          <div class="flash flash-{{ category }}">{{ message }}</div>
        {% endfor %}
      </div>
    {% endif %}
  {% endwith %}
```
- Define blocks: {% block styles %}, {% block content %}, {% block scripts %}
- Footer is already in base.html (extracted from homepage) — same dark brown footer used on every page

---

## FILES TO PRODUCE
Generate each file completely — no stubs, no TODOs.

---

### FILE 1: app/templates/auth/register.html

**Layout:** Full page centered card, max-width 480px, white card on #FFECD6 background, vertically centered with padding-top 80px

**Content:**
- Logo image at top center of card (height 48px, centered)
- H1: "Create Account" — DynaPuff, #3d2c00, centered
- Subtitle: "Join the game. Climb the leaderboard." — Comfortaa, muted, centered
- Form fields (Flask-WTF, render each field manually for full styling control):
  - Username input
  - Email input
  - Password input (type=password)
  - Confirm Password input (type=password)
  - Submit button: full-width, primary button style, label "Create Account"
- Below form: "Already have an account? Log in →" — Comfortaa small, link in #FFCC79
- Field error display: if field.errors, show each error in small red Comfortaa text below the field, with red border on the input
- CSRF hidden field must be included: `{{ form.hidden_tag() }}`

**Validation UX:**
- On input focus: border brightens to #FFCC79 with soft glow (box-shadow 0 0 0 3px rgba(255,204,121,0.25))
- Error state: border turns #fca5a5, error message below in #991b1b small Comfortaa

---

### FILE 2: app/templates/auth/login.html

**Layout:** Identical centering and card structure to register.html

**Content:**
- Logo at top center
- H1: "Welcome Back" — DynaPuff
- Subtitle: "Log in to keep playing." — Comfortaa muted
- Form fields:
  - Username input
  - Password input
  - Submit button: full-width primary, label "Log In"
- Below form: "Don't have an account? Register →" link in #FFCC79
- CSRF hidden field
- Same error display pattern as register

---

### FILE 3: app/templates/game/select.html

**Layout:** Full page, centered content, padding-top 80px, background #FFECD6

**Content:**
- H1: "Choose Your Difficulty" — DynaPuff, large, centered, #3d2c00
- Subtitle: "Higher difficulty = bigger multiplier. You get 10 attempts regardless." — Comfortaa centered muted
- 3 difficulty cards in a horizontal row (stack on mobile), each is a <form> POST to /game/start with hidden input `difficulty`:

  **Easy card:**
  - Top accent bar: #86efac (8px, rounded top)
  - Title: "Easy" — DynaPuff
  - Range: "0 – 99" — DynaPuff large, #FFCC79
  - Multiplier badge: "1× Multiplier" — Comfortaa, bg #bbf7d0, text #166534, rounded-full
  - Tagline: "Perfect for warming up" — Comfortaa muted
  - Button: "Play Easy" — full-width, primary style

  **Moderate card:** accent #fcd34d, range 0–999, multiplier 2×, badge amber, button "Play Moderate"
  **Expert card:** accent #fca5a5, range 0–9999, multiplier 3×, badge red, button "Play Expert"

- If user has an active game: show a warning banner above the cards: "⚠️ You have an active game in progress. Starting a new game will forfeit it."

Styled as a rounded-2xl amber warning box (#fef3c7 bg, #92400e text, Comfortaa)

- Card hover: lift (translateY -6px), transition 250ms ease
- Each card: white bg, rounded-3xl, shadow, equal width, max-width 300px

---

### FILE 4: app/templates/game/play.html

**Layout:** Two-column on desktop (left: game UI, right: guess history), single column on mobile. Max-width 960px, centered, padding-top 60px

**Left Column — Game UI:**
- Header row: Difficulty badge (pill) + "Attempt X of 10" label (Comfortaa, muted)
- Attempt progress bar: full width, background #FFF3E6, filled portion #FFCC79, height 10px, rounded-full — visually shows attempts remaining
- H2: range reminder e.g. "Guess a number between 0 and 99" — DynaPuff, #3d2c00
- Guess input: large, centered, number type, min/max set to difficulty range, full-width, input style from design system, font-size 1.5rem, text-center
- Submit button: full-width primary "Submit Guess →" — DynaPuff
- Disable input + button if game status is not 'active', show message "Game Over" in muted Comfortaa

**Right Column — Guess History:**
- Title: "Your Guesses" — DynaPuff small, #3d2c00
- If no guesses yet: "No guesses yet — take your first shot!" italic Comfortaa muted
- List of guess rows (most recent first), each row:
  - Guess number (bold DynaPuff)
  - Result indicator: "↑ Too High" (red #991b1b) or "↓ Too Low" (green #166534) or "✓ Correct!" (gold #FFCC79) — Comfortaa font-semibold
  - Subtle divider between rows
- Rows animate in: CSS `@keyframes slideIn` from opacity 0 translateX(12px) to full — apply to each row

**Passed from route:** `game` (Game object), `guesses` (list of Guess objects ordered newest first), `config` (difficulty config dict with min, max, max_attempts)

---

### FILE 5: app/templates/game/result.html

**Layout:** Full page centered card, max-width 560px, white card, padding-top 80px

**Content:**
- If game.status == 'won':
  - Large centered emoji: 🎉
  - H1: "You Got It!" — DynaPuff, #3d2c00
  - Score display: large DynaPuff number in #FFCC79 with label "points" below in Comfortaa muted
  - Stats row: "Attempts used: X / 10" | "Difficulty: [badge]" — Comfortaa
  - Leaderboard rank if passed: "You ranked #N on the leaderboard!" — Comfortaa, gold accent
- If game.status == 'lost':
  - Large centered emoji: 💀
  - H1: "Better Luck Next Time" — DynaPuff
  - Reveal: "The number was [secret_number]" — DynaPuff large, #FFCC79
  - Score: "0 points" — muted
- Two buttons below (always):
  - "Play Again" → /game/select — primary button
  - "View Leaderboard" → /leaderboard — secondary button
  - Side by side, centered, gap between

---

### FILE 6: app/templates/leaderboard.html

**Layout:** Full width page, max-width 1000px centered content, padding-top 60px

**Header:**
- H1: "Leaderboard" — DynaPuff, large, centered
- Subtitle: "The top players across all difficulties." — Comfortaa muted centered

**Difficulty Filter:**
- Row of pill buttons: All | Easy | Moderate | Expert
- Active pill: #FFCC79 background, #3d2c00 text — Comfortaa font-semibold rounded-full
- Inactive pill: transparent, border #FFCC79, same shape
- Each is a link: /leaderboard?difficulty=easy etc
- Highlight the currently active filter using `request.args.get('difficulty')`

**Leaderboard Table:**
- Full width, white card container, rounded-3xl, shadow
- Columns: Rank | Player | Difficulty | Score | Date
- Rank 1–3: medal images (goldMedal, silverMedal, bronzeMedal) — same as homepage
- Rank 4+: plain bold DynaPuff number
- Top 3 rows: left border 4px solid (gold=#fbbf24, silver=#9ca3af, bronze=#d97706)
- Difficulty: badge pill (design system colors)
- Score: DynaPuff bold, #FFCC79
- Date: Comfortaa small muted, formatted as "12 May 2025"
- Row hover: background #FFF3E6 transition
- If current logged-in user appears in table: highlight their row with #FFECD6 background + small "You" pill next to username
- Empty state: centered "No scores yet — start playing!" — Comfortaa italic muted

**Passed from route:** `entries` (list), `current_difficulty` (string or None), `current_user`

---

### FILE 7: app/templates/profile.html

**Layout:** Max-width 800px, centered, padding-top 60px

**Header card:**
- White card, rounded-3xl
- Username as H1 — DynaPuff, #3d2c00
- "Member since [date]" — Comfortaa small muted
- Row of 4 stat cards inside the header card (nested):
  - Total Games | Wins | Win Rate | Best Score
  - Each: DynaPuff large number in #FFCC79, Comfortaa label below
  - Subtle inner dividers between stats

**Difficulty Breakdown:**
- Section title: "Games by Difficulty" — DynaPuff
- 3 mini cards (Easy / Moderate / Expert) each showing games played at that level
- Same accent colors as difficulty cards (green/amber/red top bar)

**Recent Games Table:**
- Title: "Recent Games" — DynaPuff
- White card, rounded-3xl
- Columns: Date | Difficulty | Result | Score | Attempts Used
- Result: "Won" in green pill or "Lost" in red pill — Comfortaa
- Score: DynaPuff bold #FFCC79
- Max 10 rows
- Empty state if no games yet

**Passed from route:** `stats` dict (total_games, total_wins, win_rate, best_score, games_by_difficulty), `recent_games` list, `user` (User object)

---

### FILE 8: app/templates/feedback.html

**Layout:** Centered card, max-width 560px, white card, padding-top 80px

**Content:**
- H1: "Submit Feedback" — DynaPuff
- Subtitle: "Tell us what you think. We read every message." — Comfortaa muted
- Form (POST to /feedback):
  - Textarea: label "Your Feedback", min 10 chars, 6 rows, full-width, input style from design system, Comfortaa font, resize vertical only
  - Submit button: full-width primary "Send Feedback →" — DynaPuff
  - CSRF hidden field
- Below form: "Your feedback will be submitted under your username." — Comfortaa small muted (since anonymous is removed)
- Success flash message rendered by base.html (no inline success state needed)

---

### FILE 9: app/templates/contact.html

**Layout:** Max-width 640px, centered, padding-top 80px

**Content:**
- H1: "Contact Us" — DynaPuff, centered
- Subtitle: "Have a question or issue? Reach out." — Comfortaa muted centered
- 3 contact cards (stacked vertically), each white card rounded-3xl:

  **Email card:**
  - Icon: ✉️ (large, centered)
  - Label: "Email" — DynaPuff
  - Value: "support@aptech.com" — Comfortaa, #FFCC79, styled as mailto link

  **Phone card:**
  - Icon: 📞
  - Label: "Phone" — DynaPuff
  - Value: "+1 (555) 000-0000" — Comfortaa muted

  **Address card:**
  - Icon: 📍
  - Label: "Address" — DynaPuff
  - Value: "123 Learning Ave, Tech City, TC 00000" — Comfortaa muted

- Below cards: link to /feedback "Want to leave feedback instead? →" — Comfortaa small, #FFCC79

---

## Global Technical Rules (apply to ALL files)

- Every file: `{% extends "base.html" %}`, `{% block styles %}`, `{% block content %}`, `{% block scripts %}`
- Custom layout CSS in `{% block styles %}` scoped to that page — never modify base.html styles from child templates
- Jinja2 auth check: `{% if current_user %}` — consistent with however auth context is set in base.html
- Image tags: always `url_for('static', filename='images/...')` — never hardcoded paths
- All forms include `{{ form.hidden_tag() }}` for CSRF
- Responsive breakpoints: mobile-first, desktop layout kicks in at 768px
- No JavaScript frameworks — vanilla JS only, and only where strictly necessary (hamburger toggle already in navbar partial)
- Every page must look intentional and complete at both 375px (mobile) and 1280px (desktop) widths
- Difficulty badges: always use the design system pill colors — never ad-hoc colors
- Do not re-implement the navbar or footer in any child template — they come from base.html

## Output
Produce all 9 files in sequence, each clearly labelled with its file path. Every file fully implemented — no placeholders, no TODOs, no "add styling here" comments.