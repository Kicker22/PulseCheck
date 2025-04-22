from app.storage import load_encounters
from app.config import ENCOUNTER_PATH

# this file will display all encounters that are discharged 
# as those are the only ones we want feedback from.
#user feedback is handled in another file.

def display_candidates(path=ENCOUNTER_PATH):

    # Load the encounters from the JSON file that are not discharged
    encounters = load_encounters(path)

    # Filter encounters that are not discharged 
    encounters = [e for e in encounters if e.get("discharged", False)]

    # Check if there are any encounters to display
    if not encounters:
        print("No encounters available for feedback.")
        return

    # Loop through the encounters and print their details   
    print("Available Encounters for Feedback:")
    print("--------------------------------------------------")

    for e in encounters:
        providers = ", ".join(p['name'] for p in e.get('providers', []))
        print(f"Encounter ID: {e['encounter_id']} | Patient: {e['patient_name']} | Unit: {e['unit']} | Providers: {providers}")

    return encounters 




