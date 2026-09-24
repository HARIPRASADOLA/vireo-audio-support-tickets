from pathlib import Path
import pandas as pd
import numpy as np

AI_FILE = Path("output/ai_categorised_tickets.csv")
VALIDATION_FILE = Path("output/validation_sample.csv")
OUTPUT_DIR = Path("output")

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

ai = pd.read_csv(AI_FILE)
validation = pd.read_csv(VALIDATION_FILE)

print("=" * 70)
print("VIREO AUDIO — AI ERROR ANALYSIS")
print("=" * 70)

# ---------------------------------------------------------
# NORMALISE VALIDATION
# ---------------------------------------------------------

validation["human_correct"] = (
    validation["human_correct"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.upper()
)

validation["ai_confidence"] = pd.to_numeric(
    validation["ai_confidence"],
    errors="coerce"
)

# Only completed reviews
reviewed = validation[
    validation["human_correct"].isin(["TRUE", "FALSE"])
].copy()

print(f"\nCompleted human reviews: {len(reviewed)}")

if len(reviewed) == 0:
    print("\nNo completed reviews found.")
    print("Complete the human_correct column first.")
    raise SystemExit

# ---------------------------------------------------------
# CONFIDENCE BUCKETS
# ---------------------------------------------------------

def confidence_bucket(value):
    if value < 0.60:
        return "Below 60%"
    elif value < 0.70:
        return "60-69%"
    elif value < 0.80:
        return "70-79%"
    elif value < 0.90:
        return "80-89%"
    else:
        return "90%+"

reviewed["confidence_bucket"] = (
    reviewed["ai_confidence"]
    .apply(confidence_bucket)
)

reviewed["correct"] = (
    reviewed["human_correct"] == "TRUE"
)

# ---------------------------------------------------------
# CONFIDENCE PERFORMANCE
# ---------------------------------------------------------

confidence_summary = (
    reviewed
    .groupby("confidence_bucket")
    .agg(
        reviewed=("correct", "count"),
        correct=("correct", "sum")
    )
    .reset_index()
)

confidence_summary["accuracy_pct"] = (
    confidence_summary["correct"]
    / confidence_summary["reviewed"]
    * 100
)

confidence_summary["error_pct"] = (
    100 - confidence_summary["accuracy_pct"]
)

confidence_order = [
    "Below 60%",
    "60-69%",
    "70-79%",
    "80-89%",
    "90%+"
]

confidence_summary["confidence_bucket"] = pd.Categorical(
    confidence_summary["confidence_bucket"],
    categories=confidence_order,
    ordered=True
)

confidence_summary = confidence_summary.sort_values(
    "confidence_bucket"
)

print("\n" + "=" * 70)
print("ACCURACY BY CONFIDENCE")
print("=" * 70)

print(
    confidence_summary.to_string(index=False)
)

# ---------------------------------------------------------
# ERROR CASES
# ---------------------------------------------------------

errors = reviewed[
    ~reviewed["correct"]
].copy()

print("\n" + "=" * 70)
print("ERRORS")
print("=" * 70)

print(
    f"\nTotal reviewed: {len(reviewed)}"
)

print(
    f"Total errors: {len(errors)}"
)

print(
    f"Error rate: "
    f"{len(errors) / len(reviewed):.2%}"
)

if len(errors) > 0:

    print("\nAI category -> human category:")

    error_pairs = (
        errors
        .groupby(
            ["ai_category", "correct_category"],
            dropna=False
        )
        .size()
        .reset_index(name="errors")
        .sort_values(
            "errors",
            ascending=False
        )
    )

    print(
        error_pairs.to_string(index=False)
    )

# ---------------------------------------------------------
# THRESHOLD ANALYSIS
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("AUTOMATION THRESHOLD ANALYSIS")
print("=" * 70)

thresholds = [
    0.50,
    0.60,
    0.70,
    0.80,
    0.90
]

threshold_results = []

for threshold in thresholds:

    accepted = reviewed[
        reviewed["ai_confidence"] >= threshold
    ]

    if len(accepted) == 0:
        continue

    accuracy = accepted["correct"].mean()

    threshold_results.append(
        {
            "threshold": threshold,
            "tickets_accepted": len(accepted),
            "share_accepted_pct":
                len(accepted) / len(reviewed) * 100,
            "accuracy_pct":
                accuracy * 100,
            "error_pct":
                (1 - accuracy) * 100
        }
    )

threshold_df = pd.DataFrame(
    threshold_results
)

print(
    threshold_df.to_string(index=False)
)

# ---------------------------------------------------------
# RECOMMENDED OPERATIONAL RULE
# ---------------------------------------------------------

# We use 80% as the initial operating threshold.
#
# This is NOT a claim that 80% is universally correct.
# It is a practical starting point that can be changed
# after more validation data is collected.

THRESHOLD = 0.80

reviewed["routing"] = np.where(
    reviewed["ai_confidence"] >= THRESHOLD,
    "AUTO",
    "HUMAN_REVIEW"
)

routing_summary = (
    reviewed["routing"]
    .value_counts()
    .rename_axis("routing")
    .reset_index(name="tickets")
)

routing_summary["share_pct"] = (
    routing_summary["tickets"]
    / len(reviewed)
    * 100
)

print("\n" + "=" * 70)
print("INITIAL ROUTING RULE")
print("=" * 70)

print(
    f"\nConfidence threshold: {THRESHOLD:.0%}"
)

print(
    routing_summary.to_string(index=False)
)

# ---------------------------------------------------------
# SAVE RESULTS
# ---------------------------------------------------------

confidence_summary.to_csv(
    OUTPUT_DIR / "confidence_accuracy.csv",
    index=False
)

threshold_df.to_csv(
    OUTPUT_DIR / "automation_thresholds.csv",
    index=False
)

errors.to_csv(
    OUTPUT_DIR / "ai_validation_errors.csv",
    index=False
)

routing_summary.to_csv(
    OUTPUT_DIR / "routing_summary.csv",
    index=False
)

print("\n" + "=" * 70)
print("FILES CREATED")
print("=" * 70)

print("output/confidence_accuracy.csv")
print("output/automation_thresholds.csv")
print("output/ai_validation_errors.csv")
print("output/routing_summary.csv")