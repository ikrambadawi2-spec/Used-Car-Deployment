# AutoValue: Used Car Price Intelligence

AutoValue is a Streamlit application for exploring used-car listings and estimating resale prices. It combines an overview of the cleaned dataset, interactive market insights, and a trained machine-learning model in one interface.

The project uses 5,871 cleaned listings. The prediction target is `Price`, expressed in Indian rupees (INR) lakhs, where 1 lakh equals INR 100,000. Estimates are based on historical listing data and should be treated as guidance, not a guaranteed sale price or professional appraisal.

## Features

- **Dataset Overview**: Summarizes listings, brands, locations, and prices; explains the dataset columns; and provides statistical summaries and interactive listing filters.
- **Price Insights**: Explores how listing prices vary by vehicle year, brand, transmission, fuel type, city, and previous ownership. Filters let you narrow the analysis by year, fuel, and transmission.
- **Car Price Prediction**: Accepts vehicle details and returns an estimated price, a suggested negotiation range, and comparisons with market medians. Preset vehicles are available for quick examples.

## Data and Model

The cleaned dataset contains the following columns:

`Price`, `Brand`, `Location`, `Year`, `Kilometers_Driven`, `Fuel_Type`, `Transmission`, `Owner_Type`, `Mileage`, `Engine`, `Power`, and `Seats`.

The prediction page loads a trained Ridge Regression pipeline and the saved input-column order. Keep these files in the project root alongside the app files:

- `cleaned_df.csv`: cleaned listings used by the overview, insights, and prediction pages
- `ridge_model.joblib`: trained prediction pipeline
- `Inputs.pkl`: expected model input-column order

`Used Cars Prices.csv` is the original dataset, and `Used Cars Regression Models with Pipeline.ipynb` contains the model development work.

## Setup and Run

From the project directory, create and activate the conda environment, install dependencies, and start Streamlit:

```powershell
conda create -n DA python=3.12 -y
conda activate DA
pip install -r requirements.txt
streamlit run Home.py
```

Streamlit prints a local URL when the app starts. Open it in a browser to use the application. The Home page provides navigation to the Price Insights and Car Price Prediction pages.

## Project Structure

```text
.
├── Home.py
├── app_theme.py
├── cleaned_df.csv
├── Inputs.pkl
├── ridge_model.joblib
├── requirements.txt
├── Used Cars Prices.csv
├── Used Cars Regression Models with Pipeline.ipynb
└── pages/
    ├── Car Price Prediction.py
    └── Price Insights.py
```
