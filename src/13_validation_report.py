from pathlib import Path
import pandas as pd

INPUT = Path("output/validation_sample.csv")
OUTPUT = Path("output/ai_validation_report.txt")

df = pd.read_csv(INPUT)

validated = df[df["correct"].isin([0, 1])].copy()

lines = []

lines.append("=" * 70)
lines.append("VIREO AUDIO — AI CATEGORY VALIDATION")
lines.append("=" * 70)

lines.append(f"\nValidation records: {len(validated):,}")

if len(validated):

    correct = int((validated["correct"] == 1).sum())
    incorrect = int((validated["correct"] == 0).sum())

    accuracy = (
        correct / len(validated) * 100
    )

    lines.append(f"Correct: {correct:,}")
    lines.append(f"Incorrect: {incorrect:,}")
    lines.append(f"Accuracy: {accuracy:.2f}%")

    # High confidence
    high = validated[
        validated["ai_review_required"] == False
    ]

    if len(high):
        high_accuracy = (
            high["correct"].mean() * 100
        )

        lines.append(
            f"\nHigh-confidence records: {len(high):,}"
        )

        lines.append(
            f"High-confidence accuracy: "
            f"{high_accuracy:.2f}%"
        )

    # Low confidence
    low = validated[
        validated["ai_review_required"] == True
    ]

    if len(low):
        low_accuracy = (
            low["correct"].mean() * 100
        )

        lines.append(
            f"\nLow-confidence records: {len(low):,}"
        )

        lines.append(
            f"Low-confidence accuracy: "
            f"{low_accuracy:.2f}%"
        )

    lines.append("\nAccuracy by AI category:")

    category_accuracy = (
        validated
        .groupby("ai_category")["correct"]
        .agg(["count", "mean"])
    )

    category_accuracy["accuracy_pct"] = (
        category_accuracy["mean"] * 100
    )

    for category, row in category_accuracy.iterrows():

        lines.append(
            f"{category}: "
            f"{int(row['count'])} records, "
            f"{row['accuracy_pct']:.2f}% accuracy"
        )

else:

    lines.append(
        "\nNo validation records have been marked yet."
    )

with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as f:

    f.write("\n".join(lines))

print("\n".join(lines))

print(
    f"\nSaved to: {OUTPUT}"
)