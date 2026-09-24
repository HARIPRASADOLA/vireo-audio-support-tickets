import streamlit as st
import pandas as pd
from pathlib import Path
import re

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Vireo Audio Support Analytics",
    page_icon="🎧",
    layout="wide"
)

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
OUTPUT = BASE / "output"

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_tickets():

    file = OUTPUT / "ai_categorised_tickets.csv"

    if file.exists():
        return pd.read_csv(file)

    return pd.read_csv(DATA / "tickets.csv")


df = load_tickets()

# =========================================================
# HEADER
# =========================================================

st.title("🎧 Vireo Audio — Support Ticket Intelligence")

st.caption(
    "AI-assisted categorisation, workload analysis and "
    "headcount decision support"
)

st.divider()

# =========================================================
# KPI SECTION
# =========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Tickets",
    f"{len(df):,}"
)

if "ai_category" in df.columns:

    col2.metric(
        "AI Categories",
        df["ai_category"].nunique()
    )

    if "ai_review_required" in df.columns:

        review_rate = (
            df["ai_review_required"]
            .mean()
            * 100
        )

        col3.metric(
            "AI Review Rate",
            f"{review_rate:.2f}%"
        )

else:

    col2.metric(
        "Categories",
        df["category"].nunique()
    )

    col3.metric(
        "AI Review Rate",
        "N/A"
    )

if "assigned_team" in df.columns:

    largest_team = (
        df["assigned_team"]
        .value_counts()
        .index[0]
    )

    col4.metric(
        "Largest Team",
        largest_team
    )

st.divider()

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🔎 Ticket Classifier",
        "📊 Team & Category",
        "📅 Monthly Trends",
        "💰 Business Case"
    ]
)

# =========================================================
# TAB 1 — CLASSIFIER
# =========================================================

with tab1:

    st.header("AI-assisted Ticket Categorisation")

    message = st.text_area(
        "Customer opening message",
        height=160,
        placeholder=(
            "Example: My earbuds stopped charging "
            "and the case is not showing any light."
        )
    )

    notes = st.text_area(
        "Agent closing note (optional)",
        height=120
    )

    if st.button(
        "Classify Ticket",
        type="primary"
    ):

        text = (
            str(message) + " " +
            str(notes)
        ).lower()

        # -------------------------------------------------
        # Lightweight transparent classifier
        # -------------------------------------------------

        rules = {

            "Billing": [
                "bill",
                "billing",
                "charged",
                "payment",
                "invoice",
                "refund amount",
                "wrong charge"
            ],

            "Returns": [
                "return",
                "send back",
                "replacement",
                "replace",
                "exchange"
            ],

            "Delivery": [
                "delivery",
                "delivered",
                "courier",
                "shipment",
                "shipping",
                "late delivery"
            ],

            "Warranty": [
                "warranty",
                "warranty claim",
                "manufacturing fault"
            ],

            "Technical": [
                "not working",
                "doesn't work",
                "not charging",
                "bluetooth",
                "connect",
                "pairing",
                "battery",
                "firmware"
            ],

            "Account": [
                "account",
                "login",
                "password",
                "sign in"
            ],

            "Product Information": [
                "specification",
                "specs",
                "features",
                "compatible",
                "compatibility"
            ],

            "Order": [
                "order",
                "order number",
                "purchase"
            ],

            "Cancellation": [
                "cancel",
                "cancellation"
            ],

            "Complaint": [
                "complaint",
                "angry",
                "disappointed",
                "terrible",
                "bad service"
            ],

            "Other": []

        }

        scores = {}

        for category, keywords in rules.items():

            score = 0

            for keyword in keywords:

                if keyword in text:
                    score += 1

            scores[category] = score

        predicted = max(
            scores,
            key=scores.get
        )

        matches = scores[predicted]

        if matches == 0:

            confidence = 0.35

        elif matches == 1:

            confidence = 0.65

        elif matches == 2:

            confidence = 0.80

        else:

            confidence = 0.92

        review_required = confidence < 0.60

        st.subheader("Classification")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Predicted Category",
            predicted
        )

        c2.metric(
            "Confidence",
            f"{confidence:.0%}"
        )

        c3.metric(
            "Human Review",
            "Required"
            if review_required
            else "Not required"
        )

        if review_required:

            st.warning(
                "Low-confidence result — "
                "send this ticket for human review."
            )

        else:

            st.success(
                "High-confidence classification."
            )

        matched = [
            k for k, v in scores.items()
            if v > 0
        ]

        if matched:

            st.write(
                "**Matched categories:**",
                ", ".join(matched)
            )

        st.info(
            "This demonstration classifier is intentionally "
            "transparent and rule-based. The production "
            "pipeline uses the AI categorisation dataset."
        )

# =========================================================
# TAB 2 — TEAM & CATEGORY
# =========================================================

with tab2:

    st.header("Team and Category Volume")

    left, right = st.columns(2)

    with left:

        st.subheader("Team Volume")

        team = (
            df["assigned_team"]
            .value_counts()
            .rename_axis("Team")
            .reset_index(name="Tickets")
        )

        st.dataframe(
            team,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            team.set_index("Team")
        )

    with right:

        st.subheader("Category Volume")

        category_column = (
            "ai_category"
            if "ai_category" in df.columns
            else "category"
        )

        category = (
            df[category_column]
            .value_counts()
            .rename_axis("Category")
            .reset_index(name="Tickets")
        )

        st.dataframe(
            category,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            category.set_index("Category")
        )

# =========================================================
# TAB 3 — MONTHLY TRENDS
# =========================================================

with tab3:

    st.header("Monthly Ticket Volume")

    data = df.copy()

    data["created_at"] = pd.to_datetime(
        data["created_at"],
        errors="coerce"
    )

    data["month"] = (
        data["created_at"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_team = (
        data.groupby(
            ["month", "assigned_team"]
        )
        .size()
        .unstack(fill_value=0)
    )

    st.subheader(
        "Monthly Volume by Team"
    )

    st.line_chart(
        monthly_team
    )

    category_column = (
        "ai_category"
        if "ai_category" in data.columns
        else "category"
    )

    monthly_category = (
        data.groupby(
            ["month", category_column]
        )
        .size()
        .unstack(fill_value=0)
    )

    st.subheader(
        "Monthly Volume by Category"
    )

    st.line_chart(
        monthly_category
    )

# =========================================================
# TAB 4 — BUSINESS CASE
# =========================================================

with tab4:

    st.header("Business Case")

    st.write(
        "FY26 planning cost standards from the Vireo "
        "support policy:"
    )

    cost_data = pd.DataFrame(
        {
            "Contact Type": [
                "Chat",
                "Email",
                "Voice callback",
                "Internal transfer",
                "Agent hour"
            ],
            "Cost (Rs)": [
                210,
                260,
                520,
                305,
                165
            ]
        }
    )

    st.dataframe(
        cost_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    if "transfers" in df.columns:

        transfers = pd.to_numeric(
            df["transfers"],
            errors="coerce"
        ).fillna(0)

        transfer_count = int(
            transfers.sum()
        )

        transfer_cost = (
            transfer_count * 305
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Recorded Transfers",
            f"{transfer_count:,}"
        )

        c2.metric(
            "Transfer Cost",
            f"Rs {transfer_cost:,.0f}"
        )

    if "ai_review_required" in df.columns:

        review_rate = (
            df["ai_review_required"]
            .mean()
            * 100
        )

        st.metric(
            "AI Review Rate",
            f"{review_rate:.2f}%"
        )

        st.caption(
            "Review rate is a workload indicator, not "
            "an AI error rate."
        )

st.divider()

st.caption(
    "Vireo Audio Support Intelligence — "
    "AI-assisted analysis prototype"
)