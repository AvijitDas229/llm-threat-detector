import pandas as pd
import numpy as np
import os

np.random.seed(42)

# Exact feature names from CIC-IDS2017 [citation:8]
FEATURES = [
    "Destination Port", "Flow Duration", "Total Fwd Packets", "Total Backward Packets",
    "Fwd Packet Length Mean", "Bwd Packet Length Mean", "Flow Bytes/s", "Flow Packets/s"
]

def generate_normal(n=50):
    return pd.DataFrame({
        "Destination Port": np.random.choice([80, 443, 22, 53], n),
        "Flow Duration": np.random.randint(1000, 500000, n),
        "Total Fwd Packets": np.random.randint(1, 20, n),
        "Total Backward Packets": np.random.randint(1, 20, n),
        "Fwd Packet Length Mean": np.random.uniform(20, 200, n),
        "Bwd Packet Length Mean": np.random.uniform(20, 200, n),
        "Flow Bytes/s": np.random.uniform(100, 50000, n),
        "Flow Packets/s": np.random.uniform(0.5, 200, n),
        "Label": "BENIGN"
    })

def generate_attack(n=50):
    # Simulate DDoS/DoS patterns: high packet counts, high rates, short durations
    return pd.DataFrame({
        "Destination Port": np.random.choice([80, 443], n),
        "Flow Duration": np.random.randint(1, 5000, n),
        "Total Fwd Packets": np.random.randint(50, 500, n),
        "Total Backward Packets": np.random.randint(0, 10, n),
        "Fwd Packet Length Mean": np.random.uniform(0, 50, n),
        "Bwd Packet Length Mean": np.random.uniform(0, 10, n),
        "Flow Bytes/s": np.random.uniform(100000, 5000000, n),
        "Flow Packets/s": np.random.uniform(1000, 50000, n),
        "Label": "DDoS"
    })

def main():
    normal = generate_normal(50)
    attack = generate_attack(50)
    df = pd.concat([normal, attack]).sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv("data/sample_data.csv", index=False)
    print(f"Generated {len(df)} rows -> data/sample_data.csv")
    print(f"Normal: {len(normal)}, Attack: {len(attack)}")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    main()