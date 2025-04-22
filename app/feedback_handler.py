from app.storage import load_encounters, save_encounters
from app.nlp_pipeline import analyze_feedback
from app.killSwitch import killSwitch
from app.analyze_feedback import analyze_feedback
from datetime import datetime, timezone

from app.config import ENCOUNTER_PATH

#function that prompts user to proceed or decline leaving feedback
def user_wants_to_proceed(encounter_id):
 while True:
    confirm = input(f"Do you want to proceed with feedback for encounter {encounter_id}? (yes/no): ").strip().lower()
    print("\n--------------------------------------------------")
    #check user input and stop if user enters exit
    killSwitch(confirm)

    if confirm in ['yes', 'no']:
        if confirm == 'yes':
            return True   # Proceed
        elif confirm == 'no':
            return False  # Decline
    else:   
        print("Invalid input. Please enter 'yes' or 'no'.")


#function for handle declined feedback
def handle_declined_feedback(encounter_id, path=ENCOUNTER_PATH):
    encounters = load_encounters(path)
    encounter = next((e for e in encounters if e['encounter_id'].upper() == encounter_id.upper()), None)

    if not encounter:
        print(f"Encounter with ID {encounter_id} not found.")
        return

    if encounter.get("declined", False):
        print(f"Encounter {encounter_id} was already declined.")
        return

    encounter["declined"] = True
    save_encounters(encounters, path)
    print(f"Marked encounter {encounter_id} as declined.")

# This function handles the feedback from the user and processes it using the NLP pipeline.
def handle_feedback(encounter_id, feedback_text, path=ENCOUNTER_PATH):

    encounters = load_encounters(path)

    # Find the matching encounter
    encounter = next((e for e in encounters if e['encounter_id'].upper() == encounter_id.upper()), None)
    if not encounter:
        raise ValueError(f"Encounter with ID {encounter_id} not found.")

    print("DEBUG - Type of encounter['feedback']:", type(encounter["feedback"]))
    print("DEBUG - Value of encounter['feedback']:", encounter["feedback"])
    # Ensure this encounter hasn't already received feedback or been declined
    if encounter.get("declined", False):
        raise ValueError("Feedback was declined for this encounter.")
    if encounter["feedback"]["feedback_text"]:
        raise ValueError("Feedback already submitted for this encounter.")

    # Basic feedback quality check (optional)
    if len(feedback_text) < 10:
        raise ValueError("Feedback is too short. Please provide more detail.")

    # Analyze the feedback
    analysis_result = analyze_feedback(feedback_text)
    # Fill the predefined fields

    encounter["feedback"]["feedback_text"] = feedback_text
    encounter["feedback"]["timestamp"] = datetime.now(timezone.utc).isoformat()
    encounter["feedback"]["analyzed_feedback"]["sentiment"] = analysis_result["sentiment"]
    encounter["feedback"]["analyzed_feedback"]["sentiment_score"] = analysis_result["sentiment_score"]
    #save the themes in the feedback section of the encounter
    encounter["feedback"]["analyzed_feedback"]["themes"] = analysis_result["themes"]

    # Save the updated encounter
    save_encounters(encounters, path)

    print(f"Feedback for encounter {encounter_id} saved successfully.")

    return encounter["feedback"]  # Return just the feedback section for confirmation



