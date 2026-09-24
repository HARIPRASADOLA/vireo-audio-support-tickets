from pathlib import Path
import pandas as pd

INPUT = Path("output/ai_categorised_tickets.csv")
OUTPUT = Path("output/validation_sample.csv")

df = pd.read_csv(INPUT)

# Reproducible sample
sample_size = min(300, len(df))

sample = df.sample(
    n=sample_size,
    random_state=42
).copy()

# Keep the fields needed for human validation
columns = [
    "ticket_id",
    "customer_message",
    "agent_notes",
    "category",
    "ai_category",
    "ai_confidence",
    "ai_review_required"
]

columns = [
    c for c in columns
    if c in sample.columns
]

sample = sample[columns]

# Human reviewer columns
sample["human_category"] = ""
sample["correct"] = ""
sample["reviewer_notes"] = ""

sample.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

print("=" * 70)
print("AI VALIDATION SAMPLE")
print("=" * 70)

print(f"Full dataset: {len(df):,}")
print(f"Validation sample: {len(sample):,}")

print("\nAI category distribution:")
print(
    sample["ai_category"]
    .value_counts()
    .to_string()
)

print(f"\nSaved to: {OUTPUT}")