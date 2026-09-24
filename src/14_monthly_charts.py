from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA = Path("data/tickets.csv")
OUTPUT = Path("output")

df = pd.read_csv(DATA)

df["created_at"] = pd.to_datetime(
    df["created_at"],
    errors="coerce"
)

df["month"] = (
    df["created_at"]
    .dt.to_period("M")
    .astype(str)
)

# =========================================================
# MONTHLY CATEGORY VOLUME
# =========================================================

category_monthly = (
    df.groupby(["month", "category"])
    .size()
    .reset_index(name="tickets")
)

category_pivot = (
    category_monthly
    .pivot(
        index="month",
        columns="category",
        values="tickets"
    )
    .fillna(0)
)

category_pivot.to_csv(
    OUTPUT / "monthly_category_volume.csv"
)

plt.figure(figsize=(14, 7))

category_pivot.plot(
    kind="line",
    marker="o",
    ax=plt.gca()
)

plt.title(
    "Vireo Audio — Monthly Ticket Volume by Category"
)

plt.xlabel("Month")
plt.ylabel("Tickets")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    OUTPUT / "monthly_category_volume.png",
    dpi=200
)

plt.close()

# =========================================================
# MONTHLY TEAM VOLUME
# =========================================================

team_monthly = (
    df.groupby(["month", "assigned_team"])
    .size()
    .reset_index(name="tickets")
)

team_pivot = (
    team_monthly
    .pivot(
        index="month",
        columns="assigned_team",
        values="tickets"
    )
    .fillna(0)
)

team_pivot.to_csv(
    OUTPUT / "monthly_team_volume.csv"
)

plt.figure(figsize=(14, 7))

team_pivot.plot(
    kind="line",
    marker="o",
    ax=plt.gca()
)

plt.title(
    "Vireo Audio — Monthly Ticket Volume by Team"
)

plt.xlabel("Month")
plt.ylabel("Tickets")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    OUTPUT / "monthly_team_volume.png",
    dpi=200
)

plt.close()

# =========================================================
# TEAM SHARE
# =========================================================

team_total = (
    df.groupby("assigned_team")
    .size()
    .reset_index(name="tickets")
    .sort_values(
        "tickets",
        ascending=False
    )
)

team_total["share_pct"] = (
    team_total["tickets"]
    / len(df)
    * 100
)

team_total.to_csv(
    OUTPUT / "team_volume_share.csv",
    index=False
)

# =========================================================
# CATEGORY SHARE
# =========================================================

category_total = (
    df.groupby("category")
    .size()
    .reset_index(name="tickets")
    .sort_values(
        "tickets",
        ascending=False
    )
)

category_total["share_pct"] = (
    category_total["tickets"]
    / len(df)
    * 100
)

category_total.to_csv(
    OUTPUT / "category_volume_share.csv",
    index=False
)

print("=" * 70)
print("MONTHLY CHARTS CREATED")
print("=" * 70)

print("\nCategory chart:")
print("output/monthly_category_volume.png")

print("\nTeam chart:")
print("output/monthly_team_volume.png")

print("\nSupporting files:")
print("output/monthly_category_volume.csv")
print("output/monthly_team_volume.csv")
print("output/team_volume_share.csv")
print("output/category_volume_share.csv")

print("\nTOTAL TEAM VOLUME")
print(team_total.to_string(index=False))

print("\nTOTAL CATEGORY VOLUME")
print(category_total.to_string(index=False))