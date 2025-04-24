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

# Handle declined feedback
def handle_declined_feedback(encounter_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE encounters SET declined = TRUE WHERE encounter_id = %s;", (encounter_id,))
    conn.commit()
    cursor.close()
    conn.close()

    print(f"Marked encounter {encounter_id} as declined.")

# Handle feedback and write to DB
def handle_feedback(encounter_id, feedback_text, providers):
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
    

    # Save feedback_data (adapt this to save in DB or JSON)
    save_feedback_to_db(encounter_id, feedback_data)

    return feedback_data

# Detect mentioned providers from DB
def detect_mentioned_providers(feedback_text, providers):
    mentioned = []
    text_lower = feedback_text.lower()
    for provider in providers:
        provider_name = provider['name'].lower()
        if provider_name in text_lower:
            mentioned.append(provider['name'])
    return mentioned
