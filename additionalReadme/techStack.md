
## PulseCheck Tech Stack
PulseCheck is a real-time, scoreless, natural-language patient feedback platform built to reflect the emotional truth of care, tied directly to providers and clinical encounters.

This document outlines the technology stack and architectural decisions behind the MVP version.

---

## Language

**Python 3.10+**

- Chosen for its readability, strong NLP ecosystem, and quick prototyping ability.

---

## NLP / Text Analysis

- **TextBlob** – Basic sentiment analysis for MVP
- **spaCy** – Named Entity Recognition (NER) to detect provider names and roles
- **Custom Keyword-Based Theme Matching** – Loadable from `themes.json` and match key phrases for classification

*Future:* swap to `transformers` or `sentence-transformers` for deeper semantic extraction and embeddings.

---

## Data Storage

- **MVP**: JSON files (for simplicity and transparency)
- **Optional MVP**: SQLite for local persistence and query capabilities
- **Future**: PostgreSQL or other relational databases for scaling

---

## Feedback Input & Visualization (Frontend)

- **Streamlit** – Real-time web UI for:
  - Entering feedback (one-text-box form)
  - Viewing rolling feed of parsed feedback
  - Displaying sentiment trends and top themes

*Why Streamlit?* It allows rapid dashboard prototyping and interactive filters with minimal overhead.

---

## 🔍 Dashboard Features (Initial)

- Live text feedback stream
- Sentiment filters (positive, neutral, negative)
- Top theme tagging from NLP
- Attribution display: provider, role, unit

---

## 🔧 Tooling / Libraries

- `textblob`
- `spacy`
- `streamlit`
- `pandas`
- `pytest` (for testing)

Optional additions:
- `sentence-transformers` – For semantic clustering
- `flask` or `fastapi` – If backend API needed later

---

## Security & Privacy (MVP Practice)

- Use only pseudonymized/fake data
- No real PHI or patient identifiers
- All feedback tied to synthetic encounter records

---

## Dev Tooling

- **Git + GitHub** – Version control
- **pytest** – Unit testing
- **black / isort** – Code formatting and linting (optional)

---

## Summary Table

| Component         | Tool/Lib             |
|-------------------|----------------------|
| Language          | Python 3.10+         |
| Sentiment         | TextBlob             |
| NER               | spaCy                |
| Theme Matching    | Custom JSON matcher  |
| Data Storage      | JSON / SQLite        |
| Dashboard         | Streamlit            |
| API (future)      | Flask / FastAPI      |
| Testing           | pytest               |

