# PulseCheck: Implemented Features and Architecture (MVP)

This document outlines the functionality currently implemented in PulseCheck's MVP. It serves as a point-in-time reference for what has been built, tested, and verified as working in the current codebase.

---

## Core Description

PulseCheck is a real-time, natural-language patient feedback platform. It allows patients to submit unstructured feedback tied directly to specific encounters and providers. The system analyzes sentiment, detects themes, attributes providers, and stores results in a structured backend.

---

## Implemented Features

### Feedback Intake

- Command-line interface for real-time testing and feedback simulation
- Web-based form (HTML + JS) for submitting feedback via FastAPI backend
- Supports selecting discharged encounters and entering open-text responses

### Natural Language Processing

- Sentiment scoring using VADER (NLTK)
- Custom JSON-driven theme detection (e.g., cleanliness, staff friendliness)
- Provider mention detection using lowercased substring logic with name variants
- Minimum feedback quality threshold (character count)

### Feedback Attribution

- Encounter-to-provider linking through normalized tables
- Mentions are stored with direct references to provider IDs
- Each feedback entry is uniquely tied to one encounter and one feedback object

### Data Persistence

- PostgreSQL-backed relational schema
- Core tables:
  - `encounters`
  - `feedback`
  - `feedback_themes`
  - `feedback_provider_mentions`
  - `providers`
  - `encounter_providers`
- SQLite/JSON alternatives supported in dev/test modes

### Admin-Level API Endpoints

- `GET /admin/summary`: Total feedback, avg sentiment, most recent entry
- `GET /admin/themes`: Most mentioned themes + average sentiment
- `GET /admin/providerThemeScores`: Nested view of each provider's theme sentiment breakdown

### General API Endpoints

- `GET /encounters`: Fetch list of discharged encounters pending feedback
- `POST /feedback`: Submit feedback for a selected encounter
- `GET /getFeedback/{encounter_id}`: View submitted feedback by encounter ID
- `GET /providers`: List all providers with roles and IDs

---

## Frontend (MVP)

- Static HTML + JavaScript frontend:
  - Auto-loads available encounters
  - Provides single text area for feedback
  - Uses `fetch()` API calls to communicate with FastAPI backend
- Validates feedback input before submission
- Alerts user on success or error states

---

## Backend Architecture

- Built using **FastAPI**
- CORS configured for local frontend development
- Clean separation of logic into:
  - `db_scripts`: raw SQL logic and DB access
  - `app`: NLP pipeline, feedback logic, and CLI tools
  - `api`: FastAPI route handlers
- Modular, testable, and organized for expansion

---

## Testing & Local Environment

- `.env` for environment variable separation
- Postman collection available for API testing
- `venv` used for Python dependency isolation
- API runs via:
  ```bash
  uvicorn api.api_layer:app --reload
