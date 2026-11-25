# Prompt 3 – UI / Layout Design

## AI-Based Email Spam Detection Web Application

---

## 1. Framework Choice: Flask

**Flask** is used as the web framework for this project.

| Why Flask? | Reason |
|---|---|
| Lightweight | Minimal setup needed; ideal for a beginner project |
| Python-native | No context switching between languages |
| Template support | Uses Jinja2 to render HTML files from Python |
| Easy routing | `@app.route("/")` is all you need for a page |
| REST-ready | Handles JSON requests easily for the ML prediction API |

---

## 2. Page Layout Overview

```
┌─────────────────────────────────────────────────────┐
│                    HEADER                           │
│           📧 Email Spam Detector                    │
│   AI-powered spam detection using Naive Bayes       │
├─────────────────────────────────────────────────────┤
│                   ABOUT CARD                        │
│   Short description + technology badges             │
├─────────────────────────────────────────────────────┤
│                   INPUT CARD                        │
│   [ Large Textarea for email content          ]     │
│   [ Character counter                         ]     │
│   [ 🔎 Predict ]        [ 🗑️ Clear           ]      │
├─────────────────────────────────────────────────────┤
│                  RESULT CARD (hidden initially)     │
│   🚨 Spam Email  –OR–  ✅ Not Spam Email            │
│   Confidence bar + percentage                       │
│   Descriptive result message                        │
├─────────────────────────────────────────────────────┤
│                  SAMPLE EMAILS CARD                 │
│   [🚨 Spam 1] [🚨 Spam 2] [✅ Ham 1] [✅ Ham 2]    │
├─────────────────────────────────────────────────────┤
│                    FOOTER                           │
│        Academic Project | Semester 3 | Python       │
└─────────────────────────────────────────────────────┘
```

---

## 3. Component Descriptions

### Header
- **Purpose:** Identifies the application and communicates its goal.
- **Contents:** App name, emoji icon, one-line description, technology stack summary.
- **Style:** Blue gradient background, white text, centred.

### About Card
- **Purpose:** Gives the user context about what the application does.
- **Contents:** One paragraph description, coloured technology badges (Python, Flask, etc.).
- **Style:** White card with subtle border shadow.

### Input Card
- **Purpose:** The primary interaction area where users enter email content.
- **Contents:**
  - Section heading
  - Hint text
  - Large resizable `<textarea>` (8 rows minimum)
  - Live character counter
  - **Predict** button (blue gradient — primary action)
  - **Clear** button (grey with red hover — secondary/destructive action)

### Result Card
- **Purpose:** Displays the classification result clearly after prediction.
- **Hidden by default**, appears with a fade-in animation after a prediction.
- **Spam result:** Red/pink background, 🚨 icon, red confidence bar, red text.
- **Ham result:** Green background, ✅ icon, green confidence bar, green text.
- **Contents:** Result label, confidence percentage, animated progress bar, message.

### Sample Emails Card
- **Purpose:** Lets users quickly test the application without typing.
- **Contents:** Four buttons — 2 spam examples, 2 legitimate examples.
- **Style:** Spam buttons are red-tinted; ham buttons are green-tinted.

### Footer
- **Purpose:** Provides context about the project's academic nature.
- **Contents:** Project info, semester, disclaimer.
- **Style:** Dark blue background, small white text.

---

## 4. Colour Scheme

| Element | Colour | Hex |
|---|---|---|
| Header gradient start | Dark navy | `#1a365d` |
| Header gradient end | Medium blue | `#3182ce` |
| Spam result | Red | `#c53030` |
| Spam background | Light pink | `#fff5f5` |
| Ham result | Green | `#276749` |
| Ham background | Light green | `#f0fff4` |
| Card background | White | `#ffffff` |
| Page background | Light grey-blue | `#f0f4f8` |
| Body text | Dark grey | `#2d3748` |
| Muted text | Medium grey | `#718096` |

---

## 5. Typography

- **Font:** Inter (Google Fonts) with system-ui fallback.
- **Heading size:** 1.15–2.4 rem (responsive).
- **Body size:** 0.95 rem.
- **Button size:** 0.95 rem, font-weight 600.

---

## 6. Responsive Design

- Uses CSS Flexbox and Grid for layout.
- Max width of 860px centred on wide screens.
- On screens below 600px: buttons stack vertically, padding reduced.
- Textarea is fully resizable vertically.

---

## 7. Accessibility

- All interactive elements have clear focus states.
- Result area uses `aria-live="polite"` so screen readers announce changes.
- Textarea has an `aria-label` for screen reader compatibility.
- Colour is never the only indicator — icons and text also convey state.

---

## 8. Visual Indicators Summary

| State | Icon | Background | Border |
|---|---|---|---|
| Spam detected | 🚨 | Light pink | Red |
| Not spam | ✅ | Light green | Green |
| Error / warning | ⚠️ | Light yellow | Yellow |
| Loading | Spinner animation | — | — |
