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

## Output
Produce the complete `home.html` file. No placeholders, no TODOs, no stubs. Every section fully implemented, styled, and ready to render.

