import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# Vireo Audio - Business Volume Analysis
# ---------------------------------------------------------

DATA_FILE = Path("data/tickets.csv")
OUTPUT_FILE = Path("output/business_volume.txt")

# Load tickets
df = pd.read_csv(DATA_FILE)

# Total tickets
total_tickets = len(df)

print("=" * 70)
print("VIREO AUDIO — BUSINESS VOLUME ANALYSIS")
print("=" * 70)

print(f"\nTotal tickets: {total_tickets:,}")

# ---------------------------------------------------------
# CATEGORY VOLUME
# ---------------------------------------------------------

category_volume = (
    df["category"]
    .value_counts(dropna=False)
    .rename_axis("category")
    .reset_index(name="tickets")
)

category_volume["share_pct"] = (
    category_volume["tickets"]
    / total_tickets
    * 100
)

print("\n" + "=" * 70)
print("CATEGORY VOLUME")
print("=" * 70)

print(
    category_volume.to_string(
        index=False,
        formatters={
            "share_pct": "{:.2f}%".format
        }
    )
)

# ---------------------------------------------------------
# TEAM VOLUME
# ---------------------------------------------------------

team_volume = (
    df["assigned_team"]
    .value_counts(dropna=False)
    .rename_axis("assigned_team")
    .reset_index(name="tickets")
)

team_volume["share_pct"] = (
    team_volume["tickets"]
    / total_tickets
    * 100
)

print("\n" + "=" * 70)
print("TEAM VOLUME")
print("=" * 70)

print(
    team_volume.to_string(
        index=False,
        formatters={
            "share_pct": "{:.2f}%".format
        }
    )
)

# ---------------------------------------------------------
# BILLING CHECK
# ---------------------------------------------------------

billing = df[
    df["assigned_team"]
    .astype(str)
    .str.contains("billing", case=False, na=False)
]

billing_count = len(billing)
billing_pct = billing_count / total_tickets * 100

print("\n" + "=" * 70)
print("PRIYA'S BILLING CLAIM")
print("=" * 70)

print(f"Billing tickets: {billing_count:,}")
print(f"Billing share:   {billing_pct:.2f}%")
print("Priya's stated figure: approximately 22%")

# ---------------------------------------------------------
# LOGISTICS CHECK
# ---------------------------------------------------------

logistics = df[
    df["assigned_team"]
    .astype(str)
    .str.contains("logistics", case=False, na=False)
]

logistics_count = len(logistics)
logistics_pct = logistics_count / total_tickets * 100

print("\n" + "=" * 70)
print("NEHA / PRIYA LOGISTICS CLAIM")
print("=" * 70)

print(f"Logistics tickets: {logistics_count:,}")
print(f"Logistics share:   {logistics_pct:.2f}%")
print("Priya's stated figure: approximately 16%")

# ---------------------------------------------------------
# LARGEST TEAM
# ---------------------------------------------------------

largest_team = team_volume.iloc[0]

print("\n" + "=" * 70)
print("LARGEST TEAM")
print("=" * 70)

print(
    f"Team:   {largest_team['assigned_team']}"
)

print(
    f"Tickets: {int(largest_team['tickets']):,}"
)

print(
    f"Share:   {largest_team['share_pct']:.2f}%"
)

# ---------------------------------------------------------
# SAVE SUMMARY
# ---------------------------------------------------------

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    f.write("VIREO AUDIO — BUSINESS VOLUME ANALYSIS\n")
    f.write("=" * 70 + "\n\n")

    f.write(
        f"Total tickets: {total_tickets:,}\n\n"
    )

    f.write("CATEGORY VOLUME\n")
    f.write("-" * 70 + "\n")
    f.write(
        category_volume.to_string(
            index=False
        )
    )

    f.write("\n\nTEAM VOLUME\n")
    f.write("-" * 70 + "\n")
    f.write(
        team_volume.to_string(
            index=False
        )
    )

    f.write("\n\nBILLING CHECK\n")
    f.write("-" * 70 + "\n")
    f.write(
        f"Billing tickets: {billing_count:,}\n"
    )
    f.write(
        f"Billing share: {billing_pct:.2f}%\n"
    )

    f.write("\nLOGISTICS CHECK\n")
    f.write("-" * 70 + "\n")
    f.write(
        f"Logistics tickets: {logistics_count:,}\n"
    )
    f.write(
        f"Logistics share: {logistics_pct:.2f}%\n"
    )

print("\nAnalysis saved to:")
print(OUTPUT_FILE)