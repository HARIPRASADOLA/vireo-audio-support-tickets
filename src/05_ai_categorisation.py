from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# ---------------------------------------------------------
# VIREO AUDIO — AI-ASSISTED TICKET CATEGORISATION
# ---------------------------------------------------------

DATA_FILE = Path("data/tickets.csv")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = pd.read_csv(DATA_FILE)

print("=" * 70)
print("VIREO AUDIO — AI-ASSISTED CATEGORISATION")
print("=" * 70)

print(f"\nTotal tickets: {len(df):,}")

# ---------------------------------------------------------
# PREPARE TEXT
# ---------------------------------------------------------

df["customer_message"] = (
    df["customer_message"]
    .fillna("")
    .astype(str)
)

df["agent_notes"] = (
    df["agent_notes"]
    .fillna("")
    .astype(str)
)

# Combine both text fields.
# Customer message tells us what the customer needed.
# Agent notes often contain the actual resolution/problem type.

df["combined_text"] = (
    "CUSTOMER: "
    + df["customer_message"]
    + " AGENT: "
    + df["agent_notes"]
)

# ---------------------------------------------------------
# REMOVE EMPTY / MISSING CATEGORIES
# ---------------------------------------------------------

model_df = df[
    df["category"].notna()
    & (df["category"].astype(str).str.strip() != "")
].copy()

model_df["category"] = (
    model_df["category"]
    .astype(str)
    .str.strip()
)

print(
    f"Tickets available for training: {len(model_df):,}"
)

print(
    f"Number of existing categories: "
    f"{model_df['category'].nunique()}"
)

print("\nExisting categories:")

print(
    model_df["category"]
    .value_counts()
    .to_string()
)

# ---------------------------------------------------------
# REMOVE CATEGORIES WITH ONLY ONE EXAMPLE
# ---------------------------------------------------------
#
# Stratified train/test splitting cannot reliably evaluate
# a class that appears only once.

category_counts = model_df["category"].value_counts()

valid_categories = category_counts[
    category_counts >= 2
].index

model_df = model_df[
    model_df["category"].isin(valid_categories)
].copy()

print(
    f"\nTickets after minimum-category filter: "
    f"{len(model_df):,}"
)

# ---------------------------------------------------------
# TRAIN / TEST SPLIT
# ---------------------------------------------------------

X = model_df["combined_text"]
y = model_df["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(
    f"\nTraining tickets: {len(X_train):,}"
)

print(
    f"Test tickets:     {len(X_test):,}"
)

# ---------------------------------------------------------
# TF-IDF + LOGISTIC REGRESSION
# ---------------------------------------------------------

model = Pipeline(
    [
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.95,
                sublinear_tf=True
            )
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced"
            )
        )
    ]
)

print("\nTraining classifier...")

model.fit(X_train, y_train)

print("Training complete.")

# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\n" + "=" * 70)
print("MODEL EVALUATION")
print("=" * 70)

print(
    f"\nAccuracy: {accuracy:.2%}"
)

print("\nClassification report:")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

# ---------------------------------------------------------
# APPLY MODEL TO ALL TICKETS
# ---------------------------------------------------------

print("\nGenerating AI categories for all tickets...")

df["ai_category"] = model.predict(
    df["combined_text"]
)

# Probability / confidence
probabilities = model.predict_proba(
    df["combined_text"]
)

df["ai_confidence"] = probabilities.max(
    axis=1
)

# ---------------------------------------------------------
# LOW-CONFIDENCE FLAG
# ---------------------------------------------------------

# We deliberately flag uncertain cases rather than pretending
# every prediction is equally reliable.

df["ai_review_required"] = (
    df["ai_confidence"] < 0.60
)

# ---------------------------------------------------------
# AGREEMENT WITH EXISTING CATEGORY
# ---------------------------------------------------------

df["category_match"] = (
    df["category"].fillna("").astype(str).str.strip()
    == df["ai_category"].fillna("").astype(str).str.strip()
)

agreement_rate = df["category_match"].mean()

review_rate = df["ai_review_required"].mean()

print("\n" + "=" * 70)
print("AI OUTPUT SUMMARY")
print("=" * 70)

print(
    f"\nExisting category / AI agreement: "
    f"{agreement_rate:.2%}"
)

print(
    f"Low-confidence AI predictions: "
    f"{review_rate:.2%}"
)

# ---------------------------------------------------------
# CATEGORY DISTRIBUTION
# ---------------------------------------------------------

print("\nAI category distribution:")

print(
    df["ai_category"]
    .value_counts()
    .to_string()
)

# ---------------------------------------------------------
# SAVE TICKET-LEVEL OUTPUT
# ---------------------------------------------------------

output_columns = [
    "ticket_id",
    "created_at",
    "customer_id",
    "order_id",
    "product_sku",
    "category",
    "ai_category",
    "ai_confidence",
    "ai_review_required",
    "assigned_team",
    "status",
    "channel",
    "customer_message",
    "agent_notes"
]

df[output_columns].to_csv(
    OUTPUT_DIR / "ai_categorised_tickets.csv",
    index=False
)

# ---------------------------------------------------------
# SAVE EVALUATION
# ---------------------------------------------------------

evaluation = pd.DataFrame(
    {
        "metric": [
            "test_accuracy",
            "existing_ai_category_agreement",
            "low_confidence_rate"
        ],
        "value": [
            accuracy,
            agreement_rate,
            review_rate
        ]
    }
)

evaluation.to_csv(
    OUTPUT_DIR / "ai_model_evaluation.csv",
    index=False
)

# ---------------------------------------------------------
# CONFUSION / AGREEMENT TABLE
# ---------------------------------------------------------

comparison = pd.crosstab(
    df["category"],
    df["ai_category"],
    margins=True
)

comparison.to_csv(
    OUTPUT_DIR / "category_comparison.csv"
)

print("\n" + "=" * 70)
print("FILES CREATED")
print("=" * 70)

print(
    "output/ai_categorised_tickets.csv"
)

print(
    "output/ai_model_evaluation.csv"
)

print(
    "output/category_comparison.csv"
)

print("\nAI categorisation complete.")