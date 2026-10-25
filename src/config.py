import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.8-flash"  # Updated from gemini-1.5-flash

# Experiment Configuration
NUM_NORMAL_SAMPLES = 50
NUM_ATTACK_SAMPLES = 50
RANDOM_SEED = 42

# Paths
DATA_DIR = "data"
RESULTS_DIR = "results"

# The 8 features we'll use (kept small for clear LLM prompts)
FEATURE_COLUMNS = [
    "Destination Port",
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Fwd Packet Length Mean",
    "Bwd Packet Length Mean",
    "Flow Bytes/s",
    "Flow Packets/s",
]