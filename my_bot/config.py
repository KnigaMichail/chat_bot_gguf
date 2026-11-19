# config.py
import os
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")
MODEL_PATH = os.getenv("MODEL_PATH")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.3))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 350))

