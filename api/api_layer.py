from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from utils.token_utils import SECRET_KEY, ALGORITHM

from db_scripts.fetch_discharged_encounters import fetch_discharged_encounters
from app.nlp_pipeline import analyze_feedback
from app.feedback_handler import detect_mentioned_providers
from db_scripts.db_utils import (
    save_feedback_to_db,
    fetch_providers_for_encounter,
    fetch_feedback_for_encounter,
    fetch_all_providers,
    fetch_theme_summary,
    fetch_provider_themes_summary,
    fetch_admin_summary,
    fetch_theme_summary_for_admin,
    fetch_unit_performance,
    fetch_sentiment_over_time,
    fetch_all_providers,
    fetch_encounter_details
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


# Serve everything inside /frontend as static
app.mount("/static", StaticFiles(directory="frontend"), name="static")

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
    feedback = fetch_feedback_for_encounter(encounter_id.lower())
    if feedback:
        return feedback
    raise HTTPException(status_code=404, detail=f"No feedback found for encounter {encounter_id}")

# Fetch encounter details for a specific encounter
@app.get("/encounter/{encounter_id}")
def get_encounter(encounter_id: str):
    encounter = fetch_encounter_details(encounter_id)
    if not encounter:
        raise HTTPException(status_code=404, detail="Encounter not found")
    return encounter

@app.get("/validateToken")
def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return { "encounter_id": payload["encounter_id"] }
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/feedback")
def view_feedback_form(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        encounter_id = payload["encounter_id"]

        return {
            "message": "Valid token",
            "encounter_id": encounter_id
        }

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
@app.post("/feedback")
def submit_feedback(payload: FeedbackSubmission):
    try:
        # 1. NLP analysis
        analysis = analyze_feedback(payload.feedback_text)

        # 2. Get all providers
        all_providers = fetch_all_providers()

        # 3. NLP detection of provider mentions
        mentioned_providers = detect_mentioned_providers(payload.feedback_text, all_providers)

        # 4. Build full payload
        feedback_data = {
            "feedback_text": payload.feedback_text,
            "sentiment": analysis["sentiment"],
            "sentiment_score": analysis["sentiment_score"],
            "themes": analysis["themes"],
            "mentioned_providers": mentioned_providers
        }

        save_feedback_to_db(payload.encounter_id, feedback_data)

        return {"message": "Feedback submitted successfully."}

    except Exception as e:
        print(f"Error in submit_feedback: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Fetch all providers
@app.get("/providers")
def get_providers():
    return fetch_all_providers()

#Fetch providers for a specific encounter
@app.get("/providers/{encounter_id}")
def get_providers_for_encounter(encounter_id: str):
    providers = fetch_providers_for_encounter(encounter_id.lower())
    if providers:
        return providers
    raise HTTPException(status_code=404, detail=f"No providers found for encounter {encounter_id}")

# Fetch theme summary (general)
@app.get("/themeSummary")
def get_theme_summary():
    return fetch_theme_summary()

# Fetch provider theme sentiment breakdown
@app.get("/providerThemeBreakdown")
def get_provider_theme_sentiment_details():
    return fetch_provider_themes_summary()

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