from app.storage import load_encounters, save_encounters
from app.config import ENCOUNTER_PATH
from app.killSwitch import killSwitch
from datetime import datetime, timezone


def discharge_patient(path=ENCOUNTER_PATH):
    all_encounters = load_encounters(path)
    encounters = [e for e in all_encounters if not e.get("discharged", False)]

    if not encounters:
        print("No encounters available for discharge.")
        return

    print("Available Encounters for Discharge:")
    print("--------------------------------------------------")

    for e in encounters:
        providers = ", ".join(p['name'] for p in e.get('providers', []))
        print(f"Encounter ID: {e['encounter_id']} | Patient: {e['patient_name']} | Unit: {e['unit']} | Providers: {providers}")

    encounter_id = input("\nEnter the Encounter ID you would like to discharge: ").strip().upper()
    killSwitch(encounter_id)  # Check if user wants to exit
    # Check if user wants to exit using killSwitch
    if encounter_id == "EXIT":
        killSwitch(encounter_id)

    encounter = next((e for e in all_encounters if e['encounter_id'] == encounter_id), None)

    if not encounter:
        print(f"Encounter with ID {encounter_id} not found.")
        return
    
    encounter["discharged"] = True
    encounter["discharge_timestamp"] = datetime.now(timezone.utc).isoformat()

    save_encounters(all_encounters, path)
    print("\n------------------------------------------------------------------")
    print(f"Encounter ID {encounter_id} has been discharged successfully.")
    print("------------------------------------------------------------------")
    return encounter_id


def admit_patient(path=ENCOUNTER_PATH):

    all_encounters = load_encounters(path)
    encounters = [e for e in all_encounters if e.get("discharged", False)]

    if not encounters:
        print("No encounters available for admit.")
        return

    print("Available Encounters for Admit:")
    print("--------------------------------------------------")
    for e in encounters:
        providers = ", ".join(p['name'] for p in e.get('providers', []))
        print(f"Encounter ID: {e['encounter_id']} | Patient: {e['patient_name']} | Unit: {e['unit']} | Providers: {providers}")

    encounter_id = input("\nEnter the Encounter ID you would like to admit: ").strip().upper()
    killSwitch(encounter_id)  # Check if user wants to exit
    # Check if user wants to exit using killSwitch
    if encounter_id == "EXIT":
        killSwitch(encounter_id)

    encounter = next((e for e in all_encounters if e['encounter_id'] == encounter_id), None)

    if not encounter:
        print(f"Encounter with ID {encounter_id} not found.")
        return

    encounter["discharged"] = False
    encounter["admit_timestamp"] = datetime.now(timezone.utc).isoformat()

    save_encounters(all_encounters, path)

    print("\n------------------------------------------------------------------")
    print(f"Encounter ID {encounter_id} has been admitted successfully.")
    print("------------------------------------------------------------------")
    return encounter_id

    