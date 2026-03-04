from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent.parent

# edubot db
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# app database
APP_DB_USER = os.getenv("APP_DB_USER")
APP_DB_PASS = os.getenv("APP_DB_PASS")
APP_DB_HOST = os.getenv("APP_DB_HOST")
APP_DB_PORT = os.getenv("APP_DB_PORT")
APP_DB_NAME = os.getenv("APP_DB_NAME")


if __name__=="__main__":
    print(ROOT)

"""
python3 -m src.utils.settings

"""