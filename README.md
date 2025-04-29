# PulseCheck

**Real-time, scoreless patient feedback platform tied to clinical encounters.**

PulseCheck captures open-text feedback directly from patients and analyzes it for sentiment, themes, and attribution to providers and care teams. It replaces rigid survey formats with natural expression and routes insight directly to the people responsible for the care.

---

## Why PulseCheck?

- No surveys. No star ratings. Just real human feedback.
- Routes feedback to the providers, units, or departments involved
- Enables real-time visibility into how patients perceive care
- Built for transparency, reflection, and clinical trust

---

## MVP Features (Implemented)

- Free-text patient feedback intake (CLI + Web form)
- NLP pipeline:
  - Sentiment analysis using VADER (NLTK)
  - Theme detection from `themes.json` via keyword matching
  - Provider mention detection using simple name matching
- Feedback tied to:
  - Encounter
  - Unit
  - (If mentioned) Provider
- Admin-facing API:
  - Total feedback counts and sentiment averages
  - Most frequent themes and sentiment breakdowns
  - Provider performance by theme
- Frontend:
  - Lightweight web form using HTML + JavaScript
  - Auto-loads encounters, submits via FastAPI

---

## Example Flow

1. Patient is discharged from care
2. PulseCheck sends feedback or declines
3. The system analyzes tone, theme, and provider mentions
4. Feedback is attributed to:
   - A specific encounter
   - The relevant clinical unit
   - Any provider mentioned by name
5. Insights are made available via API for dashboards and summaries

---

## Tech Stack

| Component       | Tool / Library         |
|-----------------|------------------------|
| Language        | Python 3.10+           |
| API Framework   | FastAPI                |
| NLP             | NLTK (VADER), custom matcher |
| Data Storage    | PostgreSQL             |
| Frontend        | HTML + JavaScript (MVP)|
| Testing         | Pytest                 |
| Dev Tools       | Postman, venv, Git     |

---

## Getting Started

### Run the API Locally

```bash
uvicorn api.api_layer:app --reload
