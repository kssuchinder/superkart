import streamlit as st
import pandas as pd
import requests
import os

st.set_page_config(layout="wide")

st.title('SuperKart Sales Prediction Frontend')
st.write('Enter product and store details to get a sales prediction.')

# --- Configuration for Flask API --- #
# In a deployed environment, you would get this from environment variables
# For local testing, you might hardcode it or use a default
FLASK_API_URL = os.getenv('FLASK_API_URL', 'http://localhost:7860') # Default for local testing
PREDICT_ENDPOINT = f"{FLASK_API_URL}/v1/predict"

# Input fields for features
st.sidebar.header('Product Details')
product_weight = st.sidebar.number_input('Product Weight', min_value=4.0, max_value=22.0, value=12.66, step=0.1)
product_sugar_content = st.sidebar.selectbox('Product Sugar Content', ['Low Sugar', 'Regular', 'No Sugar'])
product_allocated_area = st.sidebar.number_input('Product Allocated Area', min_value=0.004, max_value=0.298, value=0.06, step=0.001, format="%.3f")
product_mrp = st.sidebar.number_input('Product MRP', min_value=32.0, max_value=266.9, value=117.08, step=0.1)
product_id_char = st.sidebar.selectbox('Product ID Character', ['FD', 'NC', 'DR'])

st.sidebar.header('Store Details')
store_size = st.sidebar.selectbox('Store Size', ['Medium', 'Small', 'High'])
store_location_city_type = st.sidebar.selectbox('Store Location City Type', ['Tier 1', 'Tier 2', 'Tier 3'])
store_type = st.sidebar.selectbox('Store Type', ['Supermarket Type1', 'Supermarket Type2', 'Departmental Store', 'Food Mart'])
store_age_years = st.sidebar.number_input('Store Age (Years)', min_value=5, max_value=35, value=16, step=1)

# Collect all inputs into a dictionary
input_data = {
    'Product_Weight': product_weight,
    'Product_Sugar_Content': product_sugar_content,
    'Product_Allocated_Area': product_allocated_area,
    'Product_MRP': product_mrp,
    'Store_Size': store_size,
    'Store_Location_City_Type': store_location_city_type,
    'Store_Type': store_type,
    'Product_Id_char': product_id_char,
    'Store_Age_Years': store_age_years
}

if st.button('Predict Sales'):
    try:
        # Make an API call to the Flask backend
        response = requests.post(PREDICT_ENDPOINT, json=input_data)

        if response.status_code == 200:
            prediction = response.json().get('prediction')
            st.success(f"Predicted Sales Total: ${prediction[0]:,.2f}")
        else:
            st.error(f"Error from API: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error(f"Connection Error: Could not connect to the Flask API at {PREDICT_ENDPOINT}. "
                 "Please ensure the Flask backend is running and the FLASK_API_URL is correctly configured.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

st.markdown("""
--- 
**How to Run This Streamlit App Locally:**
1. Save the above code as `streamlit_app.py`.
2. Ensure your Flask backend (`app.py`) is running. If running locally, start it first.
3. Open your terminal in the same directory and run: `streamlit run streamlit_app.py`
4. If deploying to GitHub Codespaces, ensure `FLASK_API_URL` is set as an environment variable to point to your Flask container.
""")
