from app.storage import load_encounters, save_encounters
from app.nlp_pipeline import analyze_feedback
from datetime import datetime, timezone

from app.config import ENCOUNTER_PATH


# This function handles the feedback from the user and processes it using the NLP pipeline.
def handle_feedback(encounter_id, feedback_text, path=ENCOUNTER_PATH):

    # Load the encounters from the JSON file
    encounters = load_encounters(path)

    #Find matching encounter by ID
    encounter = next((e for e in encounters if e['encounter_id'] == encounter_id), None)

    #handle if encounter is None:  meaning it was valid or dosen't exist
    if not encounter:
        raise ValueError(f"Encounter with ID {encounter_id} not found.")
    
    #Anylze the feedback using the NLP pipeline
    # Check that feedback_text is NOT EMPTY and is a STRING 
    if not isinstance(feedback_text, str) or len(feedback_text) < 5:
        raise ValueError("Feedback text must be a string with at least 5 characters.")
    
    # Create the feedback entry with metadata
    feedback_entry = {
        "feedback_text": feedback_text,
        #utc used for timezone consistency. 
        "timestamp": datetime.now(timezone.utc).isoformat(),  # ISO format for timestamp
        "analyzed_feedback": analyze_feedback(feedback_text)  # Analyze the feedback using the NLP pipeline
    }

    # Append the feedback entry to the encounter's feedback list
    encounter["feedback"].append(feedback_entry)

    # Save the updated encounters back to the JSON file
    save_encounters(encounters, path) 
    print(f"Feedback saved for encounter ID {encounter_id}. Was saved successfully.")
    return feedback_entry



