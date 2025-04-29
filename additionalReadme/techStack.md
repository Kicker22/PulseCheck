# PulseCheck Tech Stack

**PulseCheck** is a real-time, natural-language patient feedback platform designed to reflect the emotional truth of care. Feedback is attributed directly to providers and tied to clinical encounters, enabling meaningful insights for staff, and leadership.

This document outlines the current technology stack and architectural decisions for the MVP version.

---

## Language

**Python 3.10+**

- Clean syntax, fast prototyping, and strong NLP support.
- Powers all core logic including NLP, feedback parsing, and API.

---

## NLP / Text Analysis

| Task                  | Tool                         |
|-----------------------|------------------------------|
| Sentiment Analysis    | VADER (via `nltk`)           |
| Theme Detection       | Custom keyword matcher (JSON driven) |
| Provider Mentioning   | Lowercased substring match with name variants |
| Future Direction      | `transformers` for deeper semantic extraction |

---

## Data Storage

| Use                   | Storage Option               |
|-----------------------|------------------------------|
| MVP                   | PostgreSQL (via psycopg2)    |
| Testing / Local Dev   | SQLite or JSON (fallback)    |
| Schema                | Normalized: feedback, themes, providers, encounters |

---

## API Layer
  - fastApi
  - See api folder for routes and comments

---

## Frontend (MVP)

**HTML + JavaScript**
- This will probably change in the future, I've just used the simplest frontend setup for development

- Basic static form for submitting feedback
- Uses `fetch()` to post to FastAPI endpoints
- Postman collection available for API testing

*Future Option*: Move to React/Vue, or dashboard tooling (e.g., Streamlit, Dash)

---

## Tooling

| Tool / Library       | Purpose                     |
|----------------------|-----------------------------|
| `fastapi`            | API backend                 |
| `uvicorn`            | ASGI server                 |
| `nltk` + `vader`     | Sentiment scoring           |
| `spacy` _(optional)_ | NER / phrase detection      |
| `psycopg2`           | PostgreSQL driver           |
| `pytest`             | Testing                     |

---

## Security & Privacy

- [`This will eventually use real clinical data of some kind or company data`]
- Uses **synthetic data** only — no PHI or real patient identifiers
- Feedback is pseudonymized and attributed to dummy encounter data
- All analytics based on non-sensitive input
- I am not using real world data for development
---

## 🛠 Dev & Deployment

| Tool / Practice       | Role                        |
|-----------------------|-----------------------------|
| `venv` / `pip`        | Environment management      |
| `.env`                | Credential/config separation |
| Git + GitHub          | Version control             |
| Postman               | API development & testing   |
| Docker _(planned)_    | Deployment containerization |

---

## Summary Table

| Component         | Tool/Lib             |
|-------------------|----------------------|
| Language          | Python 3.10+         |
| Sentiment         | NLTK / VADER         |
| Theme Matching    | Custom JSON matcher  |
| Data Storage      | PostgreSQL / SQLite  |
| API               | FastAPI              |
| Frontend          | HTML + JS (MVP)      |
| Dashboard (future)| Streamlit / React    |
| Testing           | Pytest               |
| Deployment (future)| Docker / Railway / EC2 |

