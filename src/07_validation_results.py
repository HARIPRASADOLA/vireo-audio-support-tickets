from pathlib import Path
import pandas as pd

INPUT_FILE = Path("output/validation_sample.csv")
OUTPUT_FILE = Path("output/validation_results.txt")

df = pd.read_csv(INPUT_FILE)

# ---------------------------------------------------------
# NORMALISE HUMAN REVIEW
# ---------------------------------------------------------

df["human_correct"] = (
    df["human_correct"]
    .astype(str)
    .str.strip()
    .str.upper()
)

valid = df[
    df["human_correct"].isin(["TRUE", "FALSE"])
].copy()

if len(valid) == 0:
    print("No completed human reviews found.")
    print("Fill the human_correct column first.")
    raise SystemExit

# ---------------------------------------------------------
# CALCULATE RESULTS
# ---------------------------------------------------------

correct = (
    valid["human_correct"] == "TRUE"
).sum()

incorrect = (
    valid["human_correct"] == "FALSE"
).sum()

reviewed = len(valid)

accuracy = correct / reviewed
error_rate = incorrect / reviewed

print("=" * 70)
print("VIREO AUDIO — HUMAN VALIDATION RESULTS")
print("=" * 70)

print(f"\nTickets reviewed: {reviewed}")
print(f"Correct predictions: {correct}")
print(f"Incorrect predictions: {incorrect}")

print(
    f"\nObserved validation accuracy: "
    f"{accuracy:.2%}"
)

print(
    f"Observed error rate: "
    f"{error_rate:.2%}"
)

# ---------------------------------------------------------
# LOW CONFIDENCE PERFORMANCE
# ---------------------------------------------------------

valid["low_confidence"] = (
    valid["ai_confidence"] < 0.60
)

low_conf = valid[
    valid["low_confidence"]
]

high_conf = valid[
    ~valid["low_confidence"]
]

if len(low_conf) > 0:

    low_conf_accuracy = (
        (low_conf["human_correct"] == "TRUE").mean()
    )

    print(
        f"\nLow-confidence tickets reviewed: "
        f"{len(low_conf)}"
    )

    print(
        f"Low-confidence accuracy: "
        f"{low_conf_accuracy:.2%}"
    )

if len(high_conf) > 0:

    high_conf_accuracy = (
        (high_conf["human_correct"] == "TRUE").mean()
    )

    print(
        f"\nHigh-confidence tickets reviewed: "
        f"{len(high_conf)}"
    )

    print(
        f"High-confidence accuracy: "
        f"{high_conf_accuracy:.2%}"
    )

# ---------------------------------------------------------
# ERROR CATEGORIES
# ---------------------------------------------------------

errors = valid[
    valid["human_correct"] == "FALSE"
].copy()

if len(errors) > 0:

    print("\n" + "=" * 70)
    print("ERROR ANALYSIS")
    print("=" * 70)

    print(
        "\nCorrect categories for AI errors:"
    )

    print(
        errors["correct_category"]
        .fillna("Not specified")
        .value_counts()
        .to_string()
    )

# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "VIREO AUDIO — HUMAN VALIDATION RESULTS\n"
    )

    f.write("=" * 70 + "\n\n")

    f.write(
        f"Tickets reviewed: {reviewed}\n"
    )

    f.write(
        f"Correct predictions: {correct}\n"
    )

    f.write(
        f"Incorrect predictions: {incorrect}\n"
    )

    f.write(
        f"Observed validation accuracy: "
        f"{accuracy:.2%}\n"
    )

    f.write(
        f"Observed error rate: "
        f"{error_rate:.2%}\n"
    )

print(
    f"\nResults saved to {OUTPUT_FILE}"
)