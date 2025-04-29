from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
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
    fetch_feedback_for_encounter, 
    fetch_provider_themes_summary
    )



# Create a FastAPI app instance
app = FastAPI()
class FeedbackSubmission(BaseModel):
    encounter_id: str
    feedback_text: str

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for now; we can tighten this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test route to make sure it's running
@app.get("/")
def read_root():
    return {"message": "API is up and running!"}

# This route fetches all discharged encounters
@app.get("/encounters")
def get_encounters():
    encounters = fetch_discharged_encounters()
    return encounters

# This route fetches feedback for a specific encounter
@app.get("/getFeedback/{encounter_id}")
def get_feedback(encounter_id: str):
    feedback = fetch_feedback_for_encounter(encounter_id.upper())
    if feedback:
        return feedback
    else:
        raise HTTPException(status_code=404, detail=f"No feedback found for encounter {encounter_id}")
    
# This route fetches all providers
@app.get("/providers")
def get_providers():
    providers = fetch_all_providers()
    return providers

# This route fetches theme summary
@app.get("/themeSummary")
def get_theme_summary():
    theme_summary = fetch_theme_summary()
    return theme_summary

# This route fetches provider theme sentiment details
@app.get("/providerThemeBreakdown")
def get_provider_theme_sentiment_details():
    data = fetch_provider_themes_summary()
    return data


# This route fetches provider statistics for all providers
@app.get("/providerStats")
def get_provider_stats():
    stats = fetch_provider_stats()
    return stats

# This route allows users to submit feedback for a specific encounter
@app.post("/feedback")
def submit_feedback(feedback: FeedbackSubmission):
    # Fetch providers dynamically for the encounter
    providers = fetch_providers_for_encounter(feedback.encounter_id)

    # Analyze and process feedback
    analysis_result = analyze_feedback(feedback.feedback_text)
    mentioned_providers = detect_mentioned_providers(feedback.feedback_text, providers)

    feedback_data = {
        'feedback_text': feedback.feedback_text,
        'sentiment': analysis_result['sentiment'],
        'sentiment_score': analysis_result['sentiment_score'],
        'themes': analysis_result['themes'],
        'mentioned_providers': mentioned_providers
    }

    save_feedback_to_db(feedback.encounter_id, feedback_data)

    return {"message": f"Feedback submitted for encounter {feedback.encounter_id}", "feedback_data": feedback_data}
