from app.storage import load_encounters
from app.feedback_handler import handle_feedback
#Function to display the encounters and ask for feedback using
def display_encounters(encounters):

    print("--------------------------------------------------")
    print(r"""
    ______      _          _____ _               _
    | ___ \    | |        /  __ \ |             | |   
    | |_/ /   _| |___  ___| /  \/ |__   ___  ___| | __
    |  __/ | | | / __|/ _ \ |   | '_ \ / _ \/ __| |/ /
    | |  | |_| | \__ \  __/ \__/\ | | |  __/ (__|   < 
    \_|   \__,_|_|___/\___|\____/_| |_|\___|\___|_|\_\
                                                  
                                                """)
    
    print("--------------------------------------------------")
    print("\nAvailable Encounters:")
    print("--------------------------------------------------")

    # Loop through the encounters and print their details
    for e in encounters:
        providers = ", ".join(p['name'] for p in e.get('providers', []))
        print(f"Encounter ID: {e['encounter_id']} | Patient: {e['patient_name']} | Unit: {e['unit']} | Providers: {providers}")

#Main function starts the program and handles user input
def main():
    encounters = load_encounters()
    if not encounters:
        print("No encounters found.")
        return
    display_encounters(encounters)

    encounter_id = input("\nEnter the Encounter ID you would like to provide feedback for: ").strip().upper()
    feedback_text = input("Please provide your feedback: ").strip()

    try:
        feedback_entry = handle_feedback(encounter_id, feedback_text)
        print(feedback_entry)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

