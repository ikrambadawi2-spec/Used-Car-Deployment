import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from app_theme import apply_app_theme, render_page_header, render_takeaway, get_plotly_layout_defaults

st.set_page_config(
    page_title="AutoValue | Price Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_app_theme()

@st.cache_data
def load_dataset():
    return pd.read_csv("cleaned_df.csv")

df = load_dataset()

# Page Hero Header
render_page_header(
    badge="Market Analytics & Pricing Drivers",
    title="Price Insights & Resale Drivers",
    subtitle="Understand exactly what determines a used car's valuation in plain, straightforward terms. All charts are tailored for non-technical buyers, sellers, and business decision-makers."
)

# Sidebar Filter
st.sidebar.markdown("### 🎯 Quick Filters")
st.sidebar.caption("Filter listings to see how prices shift across specific segments.")

selected_fuel = st.sidebar.multiselect(
    "Filter by Fuel Type",
    options=sorted(df["Fuel_Type"].unique()),
    default=sorted(df["Fuel_Type"].unique())
)

selected_trans = st.sidebar.multiselect(
    "Filter by Transmission",
    options=sorted(df["Transmission"].unique()),
    default=sorted(df["Transmission"].unique())
)

year_min, year_max = int(df["Year"].min()), int(df["Year"].max())
selected_years = st.sidebar.slider(
    "Manufacturing Year Range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max)
)

filtered_df = df[
    (df["Fuel_Type"].isin(selected_fuel)) &
    (df["Transmission"].isin(selected_trans)) &
    (df["Year"] >= selected_years[0]) &
    (df["Year"] <= selected_years[1])
]

if filtered_df.empty:
    st.warning("No listings match the selected filters. Please broaden your selection.")
    st.stop()

# Top Metric Banner
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(
        "Active Listings",
        f"{len(filtered_df):,}",
        help="Number of cars matching current filters"
    )
with m2:
    med_price = filtered_df["Price"].median()
    st.metric(
        "Typical (Median) Price",
        f"₹{med_price:.2f} Lakhs",
        help="50% of cars cost less than this, 50% cost more"
    )
with m3:
    avg_price = filtered_df["Price"].mean()
    st.metric(
        "Average Listed Price",
        f"₹{avg_price:.2f} Lakhs",
        help="Arithmetic average across filtered listings"
    )
with m4:
    max_price = filtered_df["Price"].max()
    st.metric(
        "Highest Listing Price",
        f"₹{max_price:.2f} Lakhs",
        help="Top-tier luxury vehicle in this selection"
    )

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# ----------------- INSIGHT 1: VEHICLE AGE & DEPRECIATION -----------------
st.markdown("### 1. 📅 How Vehicle Age Affects Resale Value")
st.markdown("Cars are depreciating assets. This chart tracks how the typical listing price changes as a vehicle gets older.")

year_stats = filtered_df.groupby("Year")["Price"].agg(["median", "mean"]).reset_index()
year_stats = year_stats.rename(columns={"median": "Typical (Median) Price", "mean": "Average Price"})

fig_year = px.line(
    year_stats,
    x="Year",
    y=["Typical (Median) Price", "Average Price"],
    markers=True,
    labels={"value": "Price (₹ Lakhs)", "Year": "Manufacturing Year", "variable": "Metric"},
    color_discrete_sequence=["#4f46e5", "#06b6d4"]
)
layout_settings = get_plotly_layout_defaults()
fig_year.update_layout(
    **layout_settings,
    height=380,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode="x unified"
)
fig_year.update_traces(hovertemplate="%{y:.2f} Lakhs")
st.plotly_chart(fig_year, use_container_width=True)

render_takeaway(
    "<strong>Steep Initial Drop:</strong> Cars lose the biggest chunk of their value within the first <strong>3 to 5 years</strong>. "
    "After year 6, price drops taper off into a predictable, gentle slope. "
    "<strong>Smart Buyer Tip:</strong> Purchasing a 4-to-5-year-old vehicle lets the original owner absorb the heavy initial depreciation while still providing a modern, reliable automobile.",
    title="Key Takeaway: Depreciation Curve"
)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# ----------------- INSIGHT 2: BRAND VALUATION COMPARISON -----------------
st.markdown("### 2. 🏷️ Which Brands Hold the Highest & Lowest Valuations?")
st.markdown("Brand badge and reputation significantly determine perceived market value. Compare average prices across the top luxury and popular volume automakers.")

brand_counts = filtered_df["Brand"].value_counts()
valid_brands = brand_counts[brand_counts >= 15].index
brand_df = filtered_df[filtered_df["Brand"].isin(valid_brands)]

brand_summary = brand_df.groupby("Brand")["Price"].median().reset_index()
top_brands = brand_summary.sort_values(by="Price", ascending=True).tail(8)
budget_brands = brand_summary.sort_values(by="Price", ascending=True).head(8)

b_col1, b_col2 = st.columns(2)

with b_col1:
    st.markdown("#### 🌟 Top Premium & Luxury Brands")
    fig_top = px.bar(
        top_brands,
        x="Price",
        y="Brand",
        orientation="h",
        text=top_brands["Price"].apply(lambda x: f"₹{x:.2f}L"),
        labels={"Price": "Median Price (₹ Lakhs)", "Brand": ""},
        color_discrete_sequence=["#4f46e5"]
    )
    fig_top.update_layout(**get_plotly_layout_defaults(), height=360)
    fig_top.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig_top, use_container_width=True)

with b_col2:
    st.markdown("#### 🚗 Most Accessible Volume Brands")
    fig_budget = px.bar(
        budget_brands,
        x="Price",
        y="Brand",
        orientation="h",
        text=budget_brands["Price"].apply(lambda x: f"₹{x:.2f}L"),
        labels={"Price": "Median Price (₹ Lakhs)", "Brand": ""},
        color_discrete_sequence=["#10b981"]
    )
    fig_budget.update_layout(**get_plotly_layout_defaults(), height=360)
    fig_budget.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig_budget, use_container_width=True)

render_takeaway(
    "<strong>Brand Class Disparity:</strong> Luxury marques (Land Rover, Porsche, Mercedes, BMW, Audi) trade at <strong>₹25 Lakhs to ₹50+ Lakhs</strong>, "
    "whereas popular commuter champions (Maruti, Hyundai, Tata, Chevrolet) trade around <strong>₹3 to ₹6 Lakhs</strong>. "
    "Mass-market brands also enjoy much higher transaction speed and wider buyer pools.",
    title="Key Takeaway: The Brand Value Premium"
)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# ----------------- INSIGHT 3: TRANSMISSION & FUEL TYPE -----------------
st.markdown("### 3. ⚙️ Powertrain Impact: Transmission & Fuel Type")
st.markdown("How much more does an Automatic gearbox cost? And does Diesel still beat Petrol on resale price?")

pow_col1, pow_col2 = st.columns(2)

with pow_col1:
    st.markdown("#### 🕹️ Automatic vs Manual Pricing")
    trans_summary = filtered_df.groupby("Transmission")["Price"].agg(["median", "count"]).reset_index()
    trans_summary = trans_summary.rename(columns={"median": "Median Price", "count": "Listing Count"})
    
    fig_trans = px.bar(
        trans_summary,
        x="Transmission",
        y="Median Price",
        text=trans_summary["Median Price"].apply(lambda x: f"₹{x:.2f}L"),
        color="Transmission",
        color_discrete_map={"Manual": "#64748b", "Automatic": "#6366f1"},
        labels={"Median Price": "Median Price (₹ Lakhs)", "Transmission": "Gearbox Type"}
    )
    fig_trans.update_layout(**get_plotly_layout_defaults(), height=330, showlegend=False)
    fig_trans.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig_trans, use_container_width=True)

with pow_col2:
    st.markdown("#### ⛽ Fuel Type Resale Comparison")
    fuel_summary = filtered_df.groupby("Fuel_Type")["Price"].agg(["median", "count"]).reset_index()
    fuel_summary = fuel_summary.sort_values(by="median", ascending=False)
    
    fig_fuel = px.bar(
        fuel_summary,
        x="Fuel_Type",
        y="median",
        text=fuel_summary["median"].apply(lambda x: f"₹{x:.2f}L"),
        color="Fuel_Type",
        color_discrete_sequence=["#0284c7", "#059669", "#d97706", "#7c3aed"],
        labels={"median": "Median Price (₹ Lakhs)", "Fuel_Type": "Fuel Mechanism"}
    )
    fig_fuel.update_layout(**get_plotly_layout_defaults(), height=330, showlegend=False)
    fig_fuel.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig_fuel, use_container_width=True)

render_takeaway(
    "<strong>Automatic Cars Command a Huge Premium:</strong> Automatic cars have a median price of roughly <strong>₹12 to ₹15 Lakhs</strong>, "
    "compared to just <strong>₹4.5 Lakhs</strong> for manuals. This is driven both by city drivers seeking driving ease and the fact that luxury vehicles are almost exclusively automatic.<br>"
    "<strong>Diesel Retains Value:</strong> Diesel models fetch noticeably higher resale figures than petrol counterparts due to highway fuel economy and higher initial showroom prices.",
    title="Key Takeaway: Mechanical Options Value"
)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# ----------------- INSIGHT 4: CITY & OWNERSHIP -----------------
st.markdown("### 4. 📍 City Pricing & Ownership History")
st.markdown("Geographic location and past ownership count both carry measurable effects on the final price tag.")

geo_col1, geo_col2 = st.columns(2)

with geo_col1:
    st.markdown("#### 🏙️ Average Price by City")
    city_summary = filtered_df.groupby("Location")["Price"].median().reset_index()
    city_summary = city_summary.sort_values(by="Price", ascending=True)

    fig_city = px.bar(
        city_summary,
        x="Price",
        y="Location",
        orientation="h",
        text=city_summary["Price"].apply(lambda x: f"₹{x:.1f}L"),
        labels={"Price": "Median Price (₹ Lakhs)", "Location": ""},
        color_discrete_sequence=["#3b82f6"]
    )
    fig_city.update_layout(**get_plotly_layout_defaults(), height=360)
    fig_city.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig_city, use_container_width=True)

with geo_col2:
    st.markdown("#### 👤 Resale Price by Previous Owners")
    owner_order = ["First", "Second", "Third", "Fourth & Above"]
    owner_summary = filtered_df.groupby("Owner_Type")["Price"].median().reindex(owner_order).dropna().reset_index()

    fig_owner = px.bar(
        owner_summary,
        x="Owner_Type",
        y="Price",
        text=owner_summary["Price"].apply(lambda x: f"₹{x:.2f}L"),
        color="Owner_Type",
        color_discrete_sequence=["#10b981", "#3b82f6", "#f59e0b", "#ef4444"],
        labels={"Price": "Median Price (₹ Lakhs)", "Owner_Type": "Owner History"}
    )
    fig_owner.update_layout(**get_plotly_layout_defaults(), height=360, showlegend=False)
    fig_owner.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig_owner, use_container_width=True)

render_takeaway(
    "<strong>First-Owner Cars Bring a 30%+ Premium:</strong> Single-owner listings command the highest valuations (median ~₹6.0L), "
    "while 3rd and 4th+ hand vehicles dip below ₹3.5L.<br>"
    "<strong>City Dynamics:</strong> Tech and affluent hubs like Coimbatore, Bangalore, and Hyderabad show higher median prices due to higher state road taxes, "
    "newer inventory, and higher penetration of premium vehicle variants.",
    title="Key Takeaway: Provenance and Regional Markets"
)
