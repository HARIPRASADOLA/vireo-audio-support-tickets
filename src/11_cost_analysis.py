from pathlib import Path
import pandas as pd

TICKETS = Path("data/tickets.csv")
OUTPUT = Path("output")

df = pd.read_csv(TICKETS)

# ---------------------------------------------------------
# CONTACT COST
# ---------------------------------------------------------

channel_cost = {
    "chat": 210,
    "email": 260,
    "voice": 520,
    "social": 210
}

df["contact_cost_inr"] = (
    df["channel"]
    .str.lower()
    .map(channel_cost)
    .fillna(0)
)

# ---------------------------------------------------------
# TRANSFER COST
# ---------------------------------------------------------

df["transfers_num"] = pd.to_numeric(
    df["transfers"],
    errors="coerce"
).fillna(0)

df["transfer_cost_inr"] = (
    df["transfers_num"] * 305
)

# ---------------------------------------------------------
# TOTAL OPERATIONAL COST
# ---------------------------------------------------------

df["operational_cost_inr"] = (
    df["contact_cost_inr"]
    + df["transfer_cost_inr"]
)

print("=" * 70)
print("VIREO AUDIO — COST ANALYSIS")
print("=" * 70)

print(f"\nTotal tickets: {len(df):,}")

print(
    f"Contact cost: "
    f"₹{df['contact_cost_inr'].sum():,.2f}"
)

print(
    f"Transfer cost: "
    f"₹{df['transfer_cost_inr'].sum():,.2f}"
)

print(
    f"Total operational cost: "
    f"₹{df['operational_cost_inr'].sum():,.2f}"
)

# ---------------------------------------------------------
# CHANNEL
# ---------------------------------------------------------

channel = (
    df.groupby("channel")
    .agg(
        tickets=("ticket_id", "count"),
        contact_cost=("contact_cost_inr", "sum"),
        transfer_cost=("transfer_cost_inr", "sum"),
        total_cost=("operational_cost_inr", "sum")
    )
    .reset_index()
)

channel["avg_cost_per_ticket"] = (
    channel["total_cost"] /
    channel["tickets"]
)

print("\n" + "=" * 70)
print("CHANNEL COST")
print("=" * 70)

print(channel.to_string(index=False))

# ---------------------------------------------------------
# TEAM
# ---------------------------------------------------------

team = (
    df.groupby("assigned_team")
    .agg(
        tickets=("ticket_id", "count"),
        transfers=("transfers_num", "sum"),
        contact_cost=("contact_cost_inr", "sum"),
        transfer_cost=("transfer_cost_inr", "sum"),
        total_cost=("operational_cost_inr", "sum")
    )
    .reset_index()
)

team["volume_share_pct"] = (
    team["tickets"] /
    len(df) * 100
)

team["transfer_rate_pct"] = (
    (team["transfers"] /
     team["tickets"]) * 100
)

team["avg_cost_per_ticket"] = (
    team["total_cost"] /
    team["tickets"]
)

team = team.sort_values(
    "tickets",
    ascending=False
)

print("\n" + "=" * 70)
print("TEAM COST")
print("=" * 70)

print(team.to_string(index=False))

# ---------------------------------------------------------
# CATEGORY
# ---------------------------------------------------------

category = (
    df.groupby("category")
    .agg(
        tickets=("ticket_id", "count"),
        transfers=("transfers_num", "sum"),
        total_cost=("operational_cost_inr", "sum")
    )
    .reset_index()
)

category["volume_share_pct"] = (
    category["tickets"] /
    len(df) * 100
)

category["avg_cost_per_ticket"] = (
    category["total_cost"] /
    category["tickets"]
)

category = category.sort_values(
    "tickets",
    ascending=False
)

print("\n" + "=" * 70)
print("CATEGORY COST")
print("=" * 70)

print(category.to_string(index=False))

# ---------------------------------------------------------
# MONTH
# ---------------------------------------------------------

df["created_at"] = pd.to_datetime(
    df["created_at"],
    errors="coerce"
)

df["month"] = (
    df["created_at"]
    .dt.to_period("M")
    .astype(str)
)

monthly = (
    df.groupby("month")
    .agg(
        tickets=("ticket_id", "count"),
        total_cost=("operational_cost_inr", "sum"),
        transfers=("transfers_num", "sum")
    )
    .reset_index()
)

print("\n" + "=" * 70)
print("MONTHLY COST")
print("=" * 70)

print(monthly.to_string(index=False))

# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

channel.to_csv(
    OUTPUT / "cost_by_channel.csv",
    index=False
)

team.to_csv(
    OUTPUT / "cost_by_team.csv",
    index=False
)

category.to_csv(
    OUTPUT / "cost_by_category.csv",
    index=False
)

monthly.to_csv(
    OUTPUT / "cost_by_month.csv",
    index=False
)

print("\nSaved:")
print("output/cost_by_channel.csv")
print("output/cost_by_team.csv")
print("output/cost_by_category.csv")
print("output/cost_by_month.csv")