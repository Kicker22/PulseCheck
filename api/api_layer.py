from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from db_scripts.fetch_discharged_encounters import fetch_discharged_encounters
from app.nlp_pipeline import analyze_feedback
from app.feedback_handler import detect_mentioned_providers
from db_scripts.db_utils import (
    save_feedback_to_db,
    fetch_providers_for_encounter,
    fetch_feedback_for_encounter,
    fetch_all_providers,
    fetch_theme_summary,
    fetch_provider_stats,
    fetch_provider_themes_summary,
    fetch_admin_summary,
    fetch_theme_summary_for_admin,
    fetch_unit_performance,
    fetch_sentiment_over_time
)

# Initialize FastAPI app
app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (can restrict later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for feedback submission
class FeedbackSubmission(BaseModel):
    encounter_id: str
    feedback_text: str

# --- ROUTES ---

# Test route
@app.get("/")
def read_root():
    return {"message": "API is up and running!"}

# Fetch all discharged encounters
@app.get("/encounters")
def get_encounters():
    return fetch_discharged_encounters()

# Fetch feedback for a specific encounter
@app.get("/getFeedback/{encounter_id}")
def get_feedback(encounter_id: str):
    feedback = fetch_feedback_for_encounter(encounter_id.upper())
    if feedback:
        return feedback
    raise HTTPException(status_code=404, detail=f"No feedback found for encounter {encounter_id}")

# Submit feedback for an encounter
@app.post("/feedback")
def submit_feedback(feedback: FeedbackSubmission):
    providers = fetch_providers_for_encounter(feedback.encounter_id)
    analysis_result = analyze_feedback(feedback.feedback_text)
    mentioned_providers = detect_mentioned_providers(feedback.feedback_text, providers)

    feedback_data = {
        "feedback_text": feedback.feedback_text,
        "sentiment": analysis_result["sentiment"],
        "sentiment_score": analysis_result["sentiment_score"],
        "themes": analysis_result["themes"],
        "mentioned_providers": mentioned_providers,
    }

    save_feedback_to_db(feedback.encounter_id, feedback_data)

    return {
        "message": f"Feedback submitted for encounter {feedback.encounter_id}",
        "feedback_data": feedback_data,
    }

# Fetch all providers
@app.get("/providers")
def get_providers():
    return fetch_all_providers()

# Fetch theme summary (general)
@app.get("/themeSummary")
def get_theme_summary():
    return fetch_theme_summary()

# Fetch provider theme sentiment breakdown
@app.get("/providerThemeBreakdown")
def get_provider_theme_sentiment_details():
    return fetch_provider_themes_summary()

# Fetch provider performance statistics
@app.get("/providerStats")
def get_provider_stats():
    return fetch_provider_stats()

# --- ADMIN ROUTES ---

# Fetch admin overview summary
@app.get("/admin/summary")
def get_admin_summary():
    return fetch_admin_summary()

# Fetch admin theme summary
@app.get("/admin/themeSummary")
def get_admin_theme_summary():
    return fetch_theme_summary_for_admin()

# Fetch unit performance breakdown
@app.get("/admin/unitPerformance")
def get_admin_unit_performance():
    return fetch_unit_performance()

# Fetch sentiment over time for admin
@app.get("/admin/sentimentOverTime")
def get_admin_sentiment_over_time():
    return fetch_sentiment_over_time()