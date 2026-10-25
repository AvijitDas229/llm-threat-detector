import pandas as pd
import numpy as np
from src.config import FEATURE_COLUMNS, NUM_NORMAL_SAMPLES, NUM_ATTACK_SAMPLES, RANDOM_SEED

def load_and_prepare(csv_path: str) -> pd.DataFrame:
    """Load CIC-IDS2017 CSV and prepare a balanced sample."""
    print(f"Loading {csv_path}...")
    df = pd.read_csv(csv_path, low_memory=False)
    
    # Clean column names (they sometimes have leading spaces)
    df.columns = df.columns.str.strip()
    
    # Identify label column (usually 'Label')
    label_col = "Label"
    if label_col not in df.columns:
        raise ValueError(f"Label column not found. Columns: {df.columns.tolist()[:10]}")
    
    # Binary classification: BENIGN vs ATTACK
    df["is_attack"] = (df[label_col].str.upper() != "BENIGN").astype(int)
    
    # Replace infinities and NaNs
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=FEATURE_COLUMNS)
    
    # Sample balanced subset
    np.random.seed(RANDOM_SEED)
    normals = df[df["is_attack"] == 0].sample(NUM_NORMAL_SAMPLES, random_state=RANDOM_SEED)
    attacks = df[df["is_attack"] == 1].sample(NUM_ATTACK_SAMPLES, random_state=RANDOM_SEED)
    
    sample = pd.concat([normals, attacks]).sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)
    
    # Keep only what we need
    result = sample[FEATURE_COLUMNS + ["is_attack", label_col]].copy()
    result = result.rename(columns={label_col: "true_label"})
    
    print(f"Sampled {len(result)} rows: {NUM_NORMAL_SAMPLES} normal, {NUM_ATTACK_SAMPLES} attack")
    print(f"Attack types present: {result['true_label'].value_counts().to_dict()}")
    return result