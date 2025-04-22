import json 
import os
from app.config import ENCOUNTER_PATH

def load_encounters(path=ENCOUNTER_PATH):
    # Check if the file exists before attempting to open it
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                encounters = json.load(f)

                # Ensure feedback is always a dict with correct structure
                for e in encounters:
                    if "feedback" not in e or not isinstance(e["feedback"], dict):
                        e["feedback"] = {
                            "feedback_text": "",
                            "timestamp": "",
                            "analyzed_feedback": {
                                "sentiment": "",
                                "sentiment_score": 0.0,
                                "themes": []
                            }
                        }
                print(f"Loaded {len(encounters)} encounters.")
                return encounters

        except json.JSONDecodeError:
            print("Invalid JSON format in encounters.json. Please check the file.")
            return []
    else:
        print("File not found. Please check the path.")
        return []


#function that accepts list for encounters and saves it to our encounters.json file
def save_encounters(encounters, path='../data/encounters.json'):
    # Validates our list of encounters we get frmo out nlp pipline
    if isinstance(encounters, list):
        try:
            # Check if the directory exists, if not create it
            #then we save our encounters to the file
            # Open the file in write mode and save the encounters
            with open(path, 'w') as f:
                # Use json.dump to write the encounters to the file
                # with indentation for better readability
                json.dump(encounters, f, indent=4)
                print(f"Saved {len(encounters)} encounters to {path}.")
        except Exception as e:
            # Handle any exceptions that occur during file writing
            # such as permission errors or disk space issues
            print(f"Error saving encounters: {e}")
    else:
        # If encounters is not a list, print an error message
        # and do not attempt to save the file
        print("Encounters should be a list. Please check the input.")