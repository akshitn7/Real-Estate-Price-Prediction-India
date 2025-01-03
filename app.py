import streamlit as st
import pickle  
import numpy as np
import json
import math

model = pickle.load(open("model.pickle", "rb")) 

st.warning("Predictions will be unrealistic if the inputs are unrealistic.",icon = "🚨")
st.title("Real Estate Price Prediction")

columns = {}
with open('columns.json','r') as f:
    columns = json.load(f)

Location = columns["data columns"]
Location = [""]+Location[3:]

location = st.selectbox("Choose Location", Location)
area = st.number_input("Enter Total Area in sqft.", step = 100)
bhk = st.number_input("Enter Number of BHK", min_value=1, max_value=10, step=1)
typ = st.selectbox("Enter Type:", ['House', 'Flat', 'Villa'])

def predict_price(location, area, bhk, typ):
    loc_index = columns['data columns'].index(location)
    z = np.zeros(len(columns['data columns']))
    z[0] = math.log(area)
    z[1] = bhk
    if typ == 'House':
        typ = 1
    elif typ == 'Flat':
        typ = 2
    else:
        typ = 3
    z[2] = typ
    if loc_index >=0 :
        z[loc_index] = 1
    return math.exp(model.predict([z])[0])

if st.button("Predict Price"):
    try:
        prediction = predict_price(location, area, bhk, typ)
        if prediction < 100:
            st.success(f"The predicted price is ₹ {prediction:,.2f} L")
        else:
            st.success(f"The predicted price is ₹ {prediction/100:,.2f} Cr")
    except:
        if location == "":
            st.warning("Location field is empty")
        if area <= 0:
            st.warning("Negative area ? Really ?")