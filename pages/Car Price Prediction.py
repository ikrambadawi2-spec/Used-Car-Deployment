import streamlit as st
import pandas as pd
import numpy as np
import joblib
import sklearn
from category_encoders import BinaryEncoder


df = pd.read_csv('cleaned_df.csv')

Location = st.selectbox('Location', df['Location'].unique())

Year = st.sidebar.slider('Year', min_value = df['Year'].min(), max_value = df['Year'].max(), value = df['Year'].min())

Kilometers_Driven = st.number_input('Kilometers_Driven')

Fuel_Type = st.selectbox('Fuel_Type', df['Fuel_Type'].unique())

Transmission = st.selectbox('Transmission', df['Transmission'].unique())

Owner_Type = st.sidebar.radio('Owner_Type', df['Owner_Type'].unique())

Mileage = st.number_input('Mileage')

Engine = st.number_input('Engine')

Power = st.number_input('Power')

Seats = st.sidebar.slider('Seats', min_value = df['Seats'].min(), max_value = df['Seats'].max(), value = df['Seats'].min(), step= 1.0)

Brand = st.selectbox('Brand', df['Brand'].unique())


# Create Dataframe For Test Row
inputs = joblib.load('Inputs.pkl')
test_rows = pd.DataFrame(data= [[Location, Year, Kilometers_Driven, Fuel_Type, Transmission,
                   Owner_Type, Mileage, Engine, Power, Seats, Brand]],
                         columns= inputs)
st.dataframe(test_rows)

model = joblib.load('ridge_model.joblib')

if st.button('predict'):
    st.write(model.predict(test_rows).round(2)[0])
