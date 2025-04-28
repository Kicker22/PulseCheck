from db_config.db_test import get_connection
from app.nlp_pipeline import analyze_feedback
from app.killSwitch import killSwitch
from db_scripts.db_utils import save_feedback_to_db

# Prompt user to proceed or decline
def user_wants_to_proceed(encounter_id):
    while True:
        confirm = input(f"Do you want to proceed with feedback for encounter {encounter_id}? (yes/no): ").strip().lower()
        killSwitch(confirm)
        if confirm in ['yes', 'no']:
            return confirm == 'yes'
        print("Invalid input. Please enter 'yes' or 'no'.")

# Mark an encounter as declined by the patient
def mark_encounter_as_declined(encounter_id):
    """
    Sets the declined status for an encounter to TRUE in the database.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE encounters
                    SET declined = TRUE
                    WHERE encounter_id = %s AND declined IS DISTINCT FROM TRUE;
                """, (encounter_id,))
            conn.commit()
        print(f"Encounter {encounter_id} has been marked as declined.")
    except Exception as e:
        print(f"Error updating declined status for encounter {encounter_id}: {e}")
        raise

# Handle feedback and write to DB
def handle_feedback(encounter_id, feedback_text, providers):
    try:
        # Analyze the text
        analysis_result = analyze_feedback(feedback_text)

        # Detect providers mentioned
        mentioned_providers = detect_mentioned_providers(feedback_text, providers)

        # Combine all the feedback data
        feedback_data = {
            'feedback_text': feedback_text,
            'sentiment': analysis_result['sentiment'],
            'sentiment_score': analysis_result['sentiment_score'],
            'themes': analysis_result['themes'],
            'mentioned_providers': mentioned_providers
        }

        # Save feedback_data to DB
        save_feedback_to_db(encounter_id, feedback_data)

        return feedback_data

    except Exception as e:
        print(f"Error handling feedback for encounter {encounter_id}: {e}")
        raise

# Detect providers mentioned in feedback text
def detect_mentioned_providers(feedback_text, providers):
    mentioned = []
    text_lower = feedback_text.lower()
    for provider in providers:
        name_variants = [
            provider['name'].lower(),
            provider['name'].split()[0].lower(),  # First name
            provider['name'].split()[-1].lower()  # Last name
        ]
        for variant in name_variants:
            if variant in text_lower:
                mentioned.append({
                    'name': provider['name'],
                    'provider_id': provider['provider_id']
                })
                break  # Avoid duplicates
    return mentioned
