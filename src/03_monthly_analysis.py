from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = Path("data/tickets.csv")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

df = pd.read_csv(DATA_FILE)

df["created_at"] = pd.to_datetime(
    df["created_at"],
    errors="coerce"
)

# Remove rows where creation date could not be parsed
df = df.dropna(subset=["created_at"]).copy()

# Month
df["month"] = df["created_at"].dt.to_period("M").astype(str)

print("=" * 70)
print("VIREO AUDIO — MONTHLY SUPPORT VOLUME")
print("=" * 70)

print(f"\nTickets analysed: {len(df):,}")
print(f"First month: {df['month'].min()}")
print(f"Last month:  {df['month'].max()}")

# ---------------------------------------------------------
# MONTHLY CATEGORY VOLUME
# ---------------------------------------------------------

monthly_category = (
    df.groupby(["month", "category"])
    .size()
    .reset_index(name="tickets")
)

monthly_category.to_csv(
    OUTPUT_DIR / "monthly_category_volume.csv",
    index=False
)

category_pivot = (
    monthly_category
    .pivot(
        index="month",
        columns="category",
        values="tickets"
    )
    .fillna(0)
)

category_pivot.to_csv(
    OUTPUT_DIR / "monthly_category_pivot.csv"
)

# ---------------------------------------------------------
# MONTHLY TEAM VOLUME
# ---------------------------------------------------------

monthly_team = (
    df.groupby(["month", "assigned_team"])
    .size()
    .reset_index(name="tickets")
)

monthly_team.to_csv(
    OUTPUT_DIR / "monthly_team_volume.csv",
    index=False
)

team_pivot = (
    monthly_team
    .pivot(
        index="month",
        columns="assigned_team",
        values="tickets"
    )
    .fillna(0)
)

team_pivot.to_csv(
    OUTPUT_DIR / "monthly_team_pivot.csv"
)

# ---------------------------------------------------------
# PRINT CATEGORY TABLE
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("MONTHLY CATEGORY VOLUME")
print("=" * 70)

print(category_pivot.to_string())

# ---------------------------------------------------------
# PRINT TEAM TABLE
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("MONTHLY TEAM VOLUME")
print("=" * 70)

print(team_pivot.to_string())

# ---------------------------------------------------------
# CATEGORY CHART
# ---------------------------------------------------------

plt.figure(figsize=(14, 7))

for category in category_pivot.columns:
    plt.plot(
        category_pivot.index,
        category_pivot[category],
        marker="o",
        label=str(category)
    )

plt.title("Vireo Audio — Monthly Ticket Volume by Category")
plt.xlabel("Month")
plt.ylabel("Number of Tickets")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "monthly_ticket_volume_by_category.png",
    dpi=150
)

plt.close()

# ---------------------------------------------------------
# TEAM CHART
# ---------------------------------------------------------

plt.figure(figsize=(14, 7))

for team in team_pivot.columns:
    plt.plot(
        team_pivot.index,
        team_pivot[team],
        marker="o",
        label=str(team)
    )

plt.title("Vireo Audio — Monthly Ticket Volume by Team")
plt.xlabel("Month")
plt.ylabel("Number of Tickets")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "monthly_ticket_volume_by_team.png",
    dpi=150
)

plt.close()

print("\n" + "=" * 70)
print("MONTHLY ANALYSIS COMPLETE")
print("=" * 70)

print("\nFiles created:")

files = [
    "monthly_category_volume.csv",
    "monthly_category_pivot.csv",
    "monthly_team_volume.csv",
    "monthly_team_pivot.csv",
    "monthly_ticket_volume_by_category.png",
    "monthly_ticket_volume_by_team.png",
]

for filename in files:
    print(f"  - output/{filename}")