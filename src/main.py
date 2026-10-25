import os
import time
import pandas as pd
from tqdm import tqdm
from src.config import FEATURE_COLUMNS, RESULTS_DIR
from src.llm_agent import query_llm
from src.baseline import train_baseline

def run_llm_demo(csv_path: str, n_rows: int = 10):
    """Run LLM on a small sample for the demo."""
    df = pd.read_csv(csv_path)
    
    # Take 5 normal + 5 attack for demo
    normal = df[df["Label"] == "BENIGN"].head(n_rows // 2)
    attack = df[df["Label"] != "BENIGN"].head(n_rows // 2)
    sample = pd.concat([normal, attack]).sample(frac=1, random_state=42)
    
    results = []
    for _, row in tqdm(sample.iterrows(), total=len(sample), desc="LLM analyzing flows"):
        flow = {col: row[col] for col in FEATURE_COLUMNS}
        llm_out = query_llm(flow)
        
        results.append({
            **flow,
            "true_label": row["Label"],
            "llm_verdict": llm_out.get("verdict"),
            "llm_attack_type": llm_out.get("attack_type"),
            "llm_confidence": llm_out.get("confidence"),
            "llm_reasoning": llm_out.get("reasoning"),
        })
        time.sleep(4)  # Rate limit
    
    return pd.DataFrame(results)

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    csv_path = "data/sample_data.csv"
    
    # 1. Baseline
    print("Training Random Forest baseline...")
    baseline_metrics = train_baseline(csv_path)
    print(f"Baseline: {baseline_metrics}\n")
    
    # 2. LLM demo
    print("Running LLM agent demo (10 flows)...")
    llm_results = run_llm_demo(csv_path, n_rows=10)
    llm_results.to_csv(f"{RESULTS_DIR}/llm_demo_results.csv", index=False)
    
    # 3. Print demo output
    print("\n" + "="*60)
    print("DEMO: LLM THREAT ANALYSIS")
    print("="*60)
    for _, row in llm_results.iterrows():
        print(f"\nTrue: {row['true_label']} | LLM: {row['llm_verdict']} ({row['llm_confidence']})")
        print(f"Reasoning: {row['llm_reasoning']}")
    
    # 4. Compare (on same 10 rows, LLM accuracy)
    llm_correct = (
        (llm_results["true_label"] == "BENIGN") & (llm_results["llm_verdict"] == "NORMAL")
    ) | (
        (llm_results["true_label"] != "BENIGN") & (llm_results["llm_verdict"] == "ATTACK")
    )
    llm_acc = llm_correct.mean()
    
    print("\n" + "="*60)
    print("COMPARISON")
    print("="*60)
    print(f"Random Forest (70/30 split): Accuracy={baseline_metrics['accuracy']:.3f}, "
          f"Precision={baseline_metrics['precision']:.3f}, Recall={baseline_metrics['recall']:.3f}")
    print(f"LLM Agent (10 samples):     Accuracy={llm_acc:.3f}")
    print(f"\nFull results saved to: {RESULTS_DIR}/llm_demo_results.csv")

if __name__ == "__main__":
    main()