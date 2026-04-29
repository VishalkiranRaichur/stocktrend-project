import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY")
    DATA_DIR = PROJECT_ROOT / "data"