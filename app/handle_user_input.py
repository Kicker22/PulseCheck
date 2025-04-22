from app.killSwitch import killSwitch

# function to handle user input for feedback
def handle_user_input():       

# Ask the user for the encounter ID and feedback text
    encounter_id = input("\nEnter the Encounter ID you would like to provide feedback for: ").strip().upper()
    feedback_text = input("Please provide your feedback: ").strip()
    return encounter_id, feedback_text
