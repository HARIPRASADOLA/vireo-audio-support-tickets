from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")

FILES = [
    "tickets.csv",
    "agents.csv",
    "orders.csv",
    "customers.csv",
    "products.csv",
]

print("=" * 70)
print("VIREO AUDIO — SUPPORT DATA PROFILE")
print("=" * 70)

for filename in FILES:
    path = DATA_DIR / filename

    print("\n" + "=" * 70)
    print(f"FILE: {filename}")
    print("=" * 70)

    df = pd.read_csv(path)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nMissing values:")
    missing = df.isna().sum()
    missing = missing[missing > 0]

    if len(missing) == 0:
        print("  None")
    else:
        for column, count in missing.items():
            percentage = count / len(df) * 100
            print(f"  - {column}: {count:,} ({percentage:.2f}%)")

    print("\nDuplicate rows:", df.duplicated().sum())

    if "ticket_id" in df.columns:
        print(
            "Duplicate ticket IDs:",
            df["ticket_id"].duplicated().sum()
        )

    if "category" in df.columns:
        print("\nExisting categories:")
        print(
            df["category"]
            .value_counts(dropna=False)
            .to_string()
        )

    if "assigned_team" in df.columns:
        print("\nAssigned teams:")
        print(
            df["assigned_team"]
            .value_counts(dropna=False)
            .to_string()
        )

    if "status" in df.columns:
        print("\nStatuses:")
        print(
            df["status"]
            .value_counts(dropna=False)
            .to_string()
        )

    if "channel" in df.columns:
        print("\nChannels:")
        print(
            df["channel"]
            .value_counts(dropna=False)
            .to_string()
        )

    if "created_at" in df.columns:
        dates = pd.to_datetime(
            df["created_at"],
            errors="coerce"
        )

        print("\nDate range:")
        print("  Start:", dates.min())
        print("  End:  ", dates.max())

print("\n" + "=" * 70)
print("PROFILE COMPLETE")
print("=" * 70)