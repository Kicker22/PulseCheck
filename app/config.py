import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ENCOUNTER_PATH = os.path.join(DATA_DIR, "encounters.json")
THEMES_PATH = os.path.join(DATA_DIR, "themes.json")
