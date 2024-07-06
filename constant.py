import os
from dotenv import load_dotenv

# load .env variables
load_dotenv()

TOKEN = os.getenv("TOKEN")

DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)
WORD_FILE = os.path.join(DATA_PATH, "words.txt")
GUILD_IDS = [833210288681517126, 1136757424758468708] # test discord server