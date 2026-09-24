from pathlib import Path
import pandas as pd

DATA_FILE = Path("data/tickets.csv")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = pd.read_csv(DATA_FILE)

# Convert timestamps
df["created_at"] = pd.to_datetime(
    df["created_at"],
    errors="coerce"
)

df["first_response_at"] = pd.to_datetime(
    df["first_response_at"],
    errors="coerce"
)

df["resolved_at"] = pd.to_datetime(
    df["resolved_at"],
    errors="coerce"
)

# ---------------------------------------------------------
# RESPONSE TIME
# ---------------------------------------------------------

df["first_response_hours"] = (
    df["first_response_at"] - df["created_at"]
).dt.total_seconds() / 3600

# ---------------------------------------------------------
# RESOLUTION TIME
# ---------------------------------------------------------

df["resolution_hours"] = (
    df["resolved_at"] - df["created_at"]
).dt.total_seconds() / 3600

# ---------------------------------------------------------
# VALIDATE NEGATIVE TIMES
# ---------------------------------------------------------

negative_response = (
    df["first_response_hours"] < 0
).sum()

negative_resolution = (
    df["resolution_hours"] < 0
).sum()

print("=" * 70)
print("VIREO AUDIO — TEAM PERFORMANCE ANALYSIS")
print("=" * 70)

print("\nNegative first-response times:", negative_response)
print("Negative resolution times:", negative_resolution)

# Replace impossible negative values with missing
df.loc[
    df["first_response_hours"] < 0,
    "first_response_hours"
] = pd.NA

df.loc[
    df["resolution_hours"] < 0,
    "resolution_hours"
] = pd.NA

# ---------------------------------------------------------
# TRANSFERS
# ---------------------------------------------------------

df["transfers_numeric"] = pd.to_numeric(
    df["transfers"],
    errors="coerce"
)

# Important:
# Blank transfers remain missing.
# We do NOT automatically convert legacy blanks to zero.

# ---------------------------------------------------------
# TEAM SUMMARY
# ---------------------------------------------------------

total_tickets = len(df)

team_summary = (
    df.groupby("assigned_team")
    .agg(
        tickets=("ticket_id", "count"),

        avg_resolution_hours=(
            "resolution_hours",
            "mean"
        ),

        median_resolution_hours=(
            "resolution_hours",
            "median"
        ),

        avg_first_response_hours=(
            "first_response_hours",
            "mean"
        ),

        median_first_response_hours=(
            "first_response_hours",
            "median"
        ),

        avg_transfers=(
            "transfers_numeric",
            "mean"
        ),

        tickets_with_transfer=(
            "transfers_numeric",
            lambda x: (x > 0).sum()
        ),

        csat_responses=(
            "csat_score",
            lambda x: x.notna().sum()
        ),

        avg_csat=(
            "csat_score",
            "mean"
        ),

        open_or_pending=(
            "status",
            lambda x: x.isin(
                ["open", "pending"]
            ).sum()
        )
    )
    .reset_index()
)

# ---------------------------------------------------------
# CALCULATE PERCENTAGES
# ---------------------------------------------------------

team_summary["volume_share_pct"] = (
    team_summary["tickets"]
    / total_tickets
    * 100
)

team_summary["transfer_rate_pct"] = (
    team_summary["tickets_with_transfer"]
    / team_summary["tickets"]
    * 100
)

team_summary["open_pending_rate_pct"] = (
    team_summary["open_or_pending"]
    / team_summary["tickets"]
    * 100
)

# Sort by volume
team_summary = team_summary.sort_values(
    "tickets",
    ascending=False
)

# ---------------------------------------------------------
# ROUND VALUES
# ---------------------------------------------------------

numeric_columns = [
    "avg_resolution_hours",
    "median_resolution_hours",
    "avg_first_response_hours",
    "median_first_response_hours",
    "avg_transfers",
    "avg_csat",
    "volume_share_pct",
    "transfer_rate_pct",
    "open_pending_rate_pct",
]

team_summary[numeric_columns] = (
    team_summary[numeric_columns].round(2)
)

# ---------------------------------------------------------
# DISPLAY
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("TEAM PERFORMANCE SUMMARY")
print("=" * 70)

print(
    team_summary.to_string(index=False)
)

# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

team_summary.to_csv(
    OUTPUT_DIR / "team_performance_summary.csv",
    index=False
)

print("\n" + "=" * 70)
print("DATA QUALITY CHECK")
print("=" * 70)

print(
    f"\nTickets: {len(df):,}"
)

print(
    "Tickets with resolution timestamp:",
    df["resolved_at"].notna().sum()
)

print(
    "Tickets with first response timestamp:",
    df["first_response_at"].notna().sum()
)

print(
    "Tickets with CSAT response:",
    df["csat_score"].notna().sum()
)

print(
    "Tickets with transfer data:",
    df["transfers_numeric"].notna().sum()
)

print("\nSaved:")
print("output/team_performance_summary.csv")