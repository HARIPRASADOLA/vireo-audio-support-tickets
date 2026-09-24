from pathlib import Path
import pandas as pd

INPUT_FILE = Path("output/ai_categorised_tickets.csv")
OUTPUT_FILE = Path("output/validation_sample.csv")

SAMPLE_SIZE = 100
RANDOM_STATE = 42

# ---------------------------------------------------------
# LOAD AI OUTPUT
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("VIREO AUDIO — HUMAN VALIDATION SAMPLE")
print("=" * 70)

print(f"\nTotal AI-classified tickets: {len(df):,}")

# ---------------------------------------------------------
# CREATE RANDOM SAMPLE
# ---------------------------------------------------------

sample_size = min(SAMPLE_SIZE, len(df))

sample = df.sample(
    n=sample_size,
    random_state=RANDOM_STATE
).copy()

# ---------------------------------------------------------
# ADD HUMAN REVIEW COLUMNS
# ---------------------------------------------------------

sample["human_correct"] = ""
sample["correct_category"] = ""
sample["review_notes"] = ""

# ---------------------------------------------------------
# SELECT REVIEW COLUMNS
# ---------------------------------------------------------

review_columns = [
    "ticket_id",
    "customer_message",
    "agent_notes",
    "category",
    "ai_category",
    "ai_confidence",
    "human_correct",
    "correct_category",
    "review_notes"
]

sample = sample[review_columns]

# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

sample.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"\nValidation sample created: "
    f"{len(sample)} tickets"
)

print(
    f"Saved to: {OUTPUT_FILE}"
)

print("\nReview instructions:")
print("1. Read customer_message.")
print("2. Read agent_notes.")
print("3. Decide whether ai_category is correct.")
print("4. Put TRUE or FALSE in human_correct.")
print("5. If FALSE, enter the correct category.")
print("6. Add a short explanation in review_notes.")

print("\nIMPORTANT:")
print("Do not use the existing category automatically as ground truth.")