import streamlit as st
import pandas as pd
import numpy as np
import joblib
from app_theme import apply_app_theme, render_page_header, render_takeaway

st.set_page_config(
    page_title="AutoValue | Car Price Predictor",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_app_theme()

@st.cache_data
def load_dataset():
    return pd.read_csv("cleaned_df.csv")

@st.cache_resource
def load_model_assets():
    inputs = joblib.load("Inputs.pkl")
    model = joblib.load("ridge_model.joblib")
    return inputs, model

df = load_dataset()
model_inputs, model = load_model_assets()

# Hero Header
render_page_header(
    badge="Machine Learning Valuation Engine",
    title="Intelligent Car Price Estimate",
    subtitle="Configure your vehicle parameters below to generate an instant, data-backed fair market price based on 5,800+ real secondary market transactions."
)

# Sidebar helper & presets
st.sidebar.markdown("### ⚡ Quick Presets")
st.sidebar.caption("Load typical specs with one click to test the model quickly.")

preset_options = {
    "Custom Configuration": None,
    "Maruti Swift (Hatchback)": {
        "Brand": "Maruti", "Location": "Mumbai", "Year": 2016, "Fuel_Type": "Petrol",
        "Transmission": "Manual", "Owner_Type": "First", "Kilometers_Driven": 42000,
        "Mileage": 20.4, "Engine": 1197.0, "Power": 83.1, "Seats": 5.0
    },
    "Honda City (Sedan)": {
        "Brand": "Honda", "Location": "Delhi", "Year": 2017, "Fuel_Type": "Petrol",
        "Transmission": "Automatic", "Owner_Type": "First", "Kilometers_Driven": 38000,
        "Mileage": 18.0, "Engine": 1497.0, "Power": 117.3, "Seats": 5.0
    },
    "Hyundai Creta (SUV)": {
        "Brand": "Hyundai", "Location": "Bangalore", "Year": 2018, "Fuel_Type": "Diesel",
        "Transmission": "Manual", "Owner_Type": "First", "Kilometers_Driven": 50000,
        "Mileage": 19.6, "Engine": 1582.0, "Power": 126.2, "Seats": 5.0
    },
    "Audi A4 (Luxury)": {
        "Brand": "Audi", "Location": "Mumbai", "Year": 2015, "Fuel_Type": "Diesel",
        "Transmission": "Automatic", "Owner_Type": "Second", "Kilometers_Driven": 62000,
        "Mileage": 17.1, "Engine": 1968.0, "Power": 174.3, "Seats": 5.0
    }
}

selected_preset = st.sidebar.selectbox("Select a Preset Vehicle", list(preset_options.keys()))
preset_data = preset_options[selected_preset]

st.sidebar.markdown("---")
st.sidebar.markdown("#### 💡 Valuation Model Info")
st.sidebar.caption(
    "• **Algorithm**: Ridge Regression with Polynomial Feature Expansion\n"
    "• **Trained on**: 5,800+ validated listings\n"
    "• **Currency**: ₹ Lakhs (1 Lakh = ₹100,000 INR)"
)

# Input Form
with st.form("valuation_form", clear_on_submit=False):
    st.markdown("### 📋 Enter Vehicle Specifications")

    col_id, col_eng, col_use = st.columns(3)

    # Column 1: Identity
    with col_id:
        st.markdown("##### 🚘 Identity & Location")
        
        default_brand = preset_data["Brand"] if preset_data else "Maruti"
        all_brands = sorted(df["Brand"].unique())
        brand_idx = all_brands.index(default_brand) if default_brand in all_brands else 0
        brand = st.selectbox("Manufacturer / Brand", all_brands, index=brand_idx)

        default_loc = preset_data["Location"] if preset_data else "Mumbai"
        all_locs = sorted(df["Location"].unique())
        loc_idx = all_locs.index(default_loc) if default_loc in all_locs else 0
        location = st.selectbox("City / Location", all_locs, index=loc_idx)

        default_year = preset_data["Year"] if preset_data else 2015
        year = st.slider(
            "Model Year",
            min_value=int(df["Year"].min()),
            max_value=int(df["Year"].max()),
            value=int(default_year),
            step=1
        )

    # Column 2: Powertrain
    with col_eng:
        st.markdown("##### ⚙️ Engine & Powertrain")

        default_fuel = preset_data["Fuel_Type"] if preset_data else "Diesel"
        all_fuels = sorted(df["Fuel_Type"].unique())
        fuel_idx = all_fuels.index(default_fuel) if default_fuel in all_fuels else 0
        fuel_type = st.selectbox("Fuel Type", all_fuels, index=fuel_idx)

        default_trans = preset_data["Transmission"] if preset_data else "Manual"
        all_trans = sorted(df["Transmission"].unique())
        trans_idx = all_trans.index(default_trans) if default_trans in all_trans else 0
        transmission = st.selectbox("Transmission Gearbox", all_trans, index=trans_idx)

        default_engine = float(preset_data["Engine"]) if preset_data else float(df["Engine"].median())
        engine = st.number_input(
            "Engine Displacement (cc)",
            min_value=float(df["Engine"].min()),
            max_value=float(df["Engine"].max()),
            value=default_engine,
            step=50.0,
            help="Typical compact cars: 1000-1200cc, Sedans: 1500cc, SUVs/Luxury: 2000cc+"
        )

        default_power = float(preset_data["Power"]) if preset_data else float(df["Power"].median())
        power = st.number_input(
            "Engine Power (bhp)",
            min_value=float(df["Power"].min()),
            max_value=float(df["Power"].max()),
            value=default_power,
            step=5.0,
            help="Brake Horsepower. City cars: 60-90 bhp, Sedans: 100-130 bhp, High Performance: 150+ bhp"
        )

    # Column 3: Usage & History
    with col_use:
        st.markdown("##### 📋 Mileage & Condition")

        default_km = int(preset_data["Kilometers_Driven"]) if preset_data else int(df["Kilometers_Driven"].median())
        kilometers_driven = st.number_input(
            "Kilometers Driven (km)",
            min_value=0,
            max_value=1000000,
            value=default_km,
            step=2000,
            help="Odometer reading in kilometers"
        )

        default_mileage = float(preset_data["Mileage"]) if preset_data else float(df["Mileage"].median())
        mileage = st.number_input(
            "Fuel Efficiency (km/l)",
            min_value=0.0,
            max_value=40.0,
            value=default_mileage,
            step=0.2,
            help="Certified mileage rating in km per liter"
        )

        default_owner = preset_data["Owner_Type"] if preset_data else "First"
        all_owners = ["First", "Second", "Third", "Fourth & Above"]
        owner_idx = all_owners.index(default_owner) if default_owner in all_owners else 0
        owner_type = st.selectbox("Previous Ownership", all_owners, index=owner_idx)

        default_seats = float(preset_data["Seats"]) if preset_data else 5.0
        seats = st.slider(
            "Seating Capacity",
            min_value=int(df["Seats"].min()),
            max_value=int(df["Seats"].max()),
            value=int(default_seats),
            step=1
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🚀 Calculate Fair Market Valuation", use_container_width=True)

# Prediction Result Display
if submitted:
    input_dict = {
        "Location": location,
        "Year": year,
        "Kilometers_Driven": kilometers_driven,
        "Fuel_Type": fuel_type,
        "Transmission": transmission,
        "Owner_Type": owner_type,
        "Mileage": mileage,
        "Engine": engine,
        "Power": power,
        "Seats": float(seats),
        "Brand": brand
    }

    input_df = pd.DataFrame([input_dict], columns=model_inputs)

    with st.spinner("Processing vehicle profile through trained machine learning model..."):
        raw_pred = float(model.predict(input_df)[0])
        pred_price = max(0.40, raw_pred)  # Floor at realistic minimum scrap value

    inr_exact = pred_price * 100000
    low_band = pred_price * 0.93
    high_band = pred_price * 1.07

    # Determine Vehicle Tier
    if pred_price < 5.0:
        tier_label = "Budget-Friendly Commuter"
        tier_badge = "background-color: #ecfdf5; color: #047857; border: 1px solid #a7f3d0;"
    elif pred_price < 12.0:
        tier_label = "Popular Mid-Market Segment"
        tier_badge = "background-color: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe;"
    elif pred_price < 25.0:
        tier_label = "Executive / Premium Tier"
        tier_badge = "background-color: #f5f3ff; color: #6d28d9; border: 1px solid #ddd6fe;"
    else:
        tier_label = "Luxury High-End Class"
        tier_badge = "background-color: #fffbeb; color: #b45309; border: 1px solid #fde68a;"

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    st.markdown("### 🎯 Valuation Appraisal Report")

    # Custom High-End Result Card
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); border: 2px solid #4f46e5; border-radius: 20px; padding: 2rem; box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.12); margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 1.25rem;">
                <span style="font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #4f46e5; background: #eef2ff; padding: 0.35rem 0.85rem; border-radius: 9999px;">
                    Estimated Market Value
                </span>
                <span style="font-size: 0.82rem; font-weight: 600; padding: 0.35rem 0.85rem; border-radius: 9999px; {tier_badge}">
                    {tier_label}
                </span>
            </div>
            <div style="display: flex; align-items: baseline; gap: 16px; flex-wrap: wrap;">
                <span style="font-family: 'Outfit', sans-serif; font-size: 3.25rem; font-weight: 800; color: #0f172a; line-height: 1;">
                    ₹ {pred_price:,.2f} Lakhs
                </span>
                <span style="font-size: 1.25rem; font-weight: 600; color: #475569;">
                    (≈ ₹ {inr_exact:,.0f} INR)
                </span>
            </div>
            <div style="margin-top: 1.25rem; padding-top: 1.25rem; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
                <div>
                    <div style="font-size: 0.82rem; color: #64748b; font-weight: 600; text-transform: uppercase;">Fair Negotiation Range (±7%)</div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #1e293b; margin-top: 2px;">
                        ₹ {low_band:,.2f} Lakhs — ₹ {high_band:,.2f} Lakhs
                    </div>
                </div>
                <div>
                    <div style="font-size: 0.82rem; color: #64748b; font-weight: 600; text-transform: uppercase;">Vehicle Profile</div>
                    <div style="font-size: 1.05rem; font-weight: 600; color: #334155; margin-top: 2px;">
                        {year} {brand} • {fuel_type} • {transmission} • {owner_type} Owner
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Benchmark comparison cards
    b1, b2, b3 = st.columns(3)
    brand_avg = df[df["Brand"] == brand]["Price"].median()
    diff_brand = pred_price - brand_avg
    
    year_avg = df[df["Year"] == year]["Price"].median()
    diff_year = pred_price - year_avg

    with b1:
        st.metric(
            f"vs {brand} Median",
            f"₹ {brand_avg:.2f}L",
            delta=f"{diff_brand:+.2f}L",
            help="Comparison against typical price for all listings of this manufacturer"
        )
    with b2:
        st.metric(
            f"vs {year} Models Median",
            f"₹ {year_avg:.2f}L",
            delta=f"{diff_year:+.2f}L",
            help="Comparison against typical price of cars manufactured in the same year"
        )
    with b3:
        overall_med = df["Price"].median()
        diff_all = pred_price - overall_med
        st.metric(
            "vs All Market Median",
            f"₹ {overall_med:.2f}L",
            delta=f"{diff_all:+.2f}L",
            help="Comparison against the overall market median (₹5.65 Lakhs)"
        )

    render_takeaway(
        f"This <strong>{year} {brand}</strong> appraisal is shaped primarily by its "
        f"<strong>{transmission}</strong> transmission, <strong>{engine:.0f} cc</strong> engine capacity, and current mileage of <strong>{kilometers_driven:,} km</strong>. "
        "A private seller should list within the upper fair range, while a buyer should negotiate toward the lower band based on physical condition and service records.",
        title="Appraisal Strategy & Negotiation Advice"
    )
