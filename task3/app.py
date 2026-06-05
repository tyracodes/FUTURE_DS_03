import streamlit as st
import pandas as pd
import plotly.express as px


# Page Configuration

st.set_page_config(
    page_title="Marketing Funnel Analysis Dashboard",
    layout="wide"
)


# Load Data

@st.cache_data
def load_data():
    import os

    file_path = os.path.join(os.path.dirname(__file__), "bank-full.csv")

    df = pd.read_csv(file_path, sep=";")
    df["converted"] = df["y"].map({"yes": 1, "no": 0})

    return df

df = load_data()


# Sidebar

st.sidebar.title("Filters")

contact_filter = st.sidebar.multiselect(
    "Contact Type",
    options=df["contact"].unique(),
    default=df["contact"].unique()
)

month_filter = st.sidebar.multiselect(
    "Month",
    options=df["month"].unique(),
    default=df["month"].unique()
)

filtered_df = df[
    (df["contact"].isin(contact_filter))
    &
    (df["month"].isin(month_filter))
]


# Title


st.title(" Marketing Funnel & Conversion Analysis Dashboard")

st.markdown("""
Analyze conversion performance, funnel drop-offs,
marketing channels, and customer behavior.
""")


# KPI SECTION


total_contacts = len(filtered_df)

customers = filtered_df["converted"].sum()

conversion_rate = (
    customers / total_contacts * 100
)

avg_duration = filtered_df["duration"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Contacts",
    f"{total_contacts:,}"
)

col2.metric(
    "Customers",
    f"{customers:,}"
)

col3.metric(
    "Conversion Rate",
    f"{conversion_rate:.2f}%"
)

col4.metric(
    "Avg Call Duration",
    f"{avg_duration:.0f} sec"
)


# FUNNEL


st.subheader("Marketing Funnel")

contacts = len(filtered_df)

reached = len(
    filtered_df[
        filtered_df["contact"] != "unknown"
    ]
)

engaged = len(
    filtered_df[
        filtered_df["duration"] > 120
    ]
)

converted = len(
    filtered_df[
        filtered_df["converted"] == 1
    ]
)

funnel_df = pd.DataFrame({
    "Stage": [
        "Contacts",
        "Reached",
        "Engaged",
        "Customers"
    ],
    "Count": [
        contacts,
        reached,
        engaged,
        converted
    ]
})

fig_funnel = px.funnel(
    funnel_df,
    x="Count",
    y="Stage",
    title="Marketing Funnel"
)

st.plotly_chart(
    fig_funnel,
    use_container_width=True
)


# CHANNEL PERFORMANCE


st.subheader("Conversion by Contact Channel")

channel_perf = (
    filtered_df
    .groupby("contact")["converted"]
    .mean()
    .reset_index()
)

channel_perf["converted"] *= 100

fig_channel = px.bar(
    channel_perf,
    x="contact",
    y="converted",
    color="contact",
    title="Channel Conversion Rate (%)"
)

st.plotly_chart(
    fig_channel,
    use_container_width=True
)


# MONTHLY PERFORMANCE


st.subheader("Monthly Conversion Performance")

monthly_perf = (
    filtered_df
    .groupby("month")["converted"]
    .mean()
    .reset_index()
)

monthly_perf["converted"] *= 100

month_order = [
    "jan","feb","mar","apr","may","jun",
    "jul","aug","sep","oct","nov","dec"
]

monthly_perf["month"] = pd.Categorical(
    monthly_perf["month"],
    categories=month_order,
    ordered=True
)

monthly_perf = monthly_perf.sort_values("month")

fig_month = px.line(
    monthly_perf,
    x="month",
    y="converted",
    markers=True,
    title="Monthly Conversion Rate (%)"
)

st.plotly_chart(
    fig_month,
    use_container_width=True
)


# CAMPAIGN EFFECTIVENESS


st.subheader("Campaign Effectiveness")

campaign_perf = (
    filtered_df
    .groupby("campaign")["converted"]
    .mean()
    .reset_index()
)

campaign_perf["converted"] *= 100

fig_campaign = px.line(
    campaign_perf.head(20),
    x="campaign",
    y="converted",
    markers=True,
    title="Conversion Rate by Number of Contacts"
)

st.plotly_chart(
    fig_campaign,
    use_container_width=True
)


# AGE ANALYSIS

st.subheader("Age Distribution")

fig_age = px.box(
    filtered_df,
    x="converted",
    y="age",
    title="Age vs Conversion"
)

st.plotly_chart(
    fig_age,
    use_container_width=True
)


# BALANCE ANALYSIS

st.subheader("Balance Distribution")

fig_balance = px.box(
    filtered_df,
    x="converted",
    y="balance",
    title="Balance vs Conversion"
)

st.plotly_chart(
    fig_balance,
    use_container_width=True
)

# INSIGHTS


st.subheader("Key Business Insights")

st.markdown("""
### Key Findings

- Funnel visualization identifies major drop-off stages.
- Channel performance reveals which contact method drives the highest conversions.
- Monthly analysis highlights seasonal conversion trends.
- Campaign analysis shows whether repeated contact improves conversion.
- Customer demographics help identify high-value customer segments.

### Recommendations

- Invest more in top-performing channels.
- Improve engagement at the largest drop-off stage.
- Increase marketing efforts during high-converting months.
- Optimize campaign contact frequency.
- Target customer profiles with higher conversion likelihood.
""")
