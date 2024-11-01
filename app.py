import streamlit as st
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

# Function to load the model
@st.cache_resource
def load_model():
    try:
        with open('svm_model.sav', 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"Error loading the model: {str(e)}")
        return None

# Load the SVM model
model = load_model()

# Create the Streamlit app
st.title('SVM Churn Prediction Model')

# Display model information
if model is not None:
    st.subheader("Model Information")
    st.write(f"Model type: {type(model).__name__}")
    if hasattr(model, 'kernel'):
        st.write(f"Kernel: {model.kernel}")

# Define the feature names
feature_names = [
    'user_id', 'REGION', 'TENURE', 'MONTANT', 'FREQUENCE_RECH', 'REVENUE',
    'ARPU_SEGMENT', 'FREQUENCE', 'DATA_VOLUME', 'ON_NET', 'ORANGE', 'TIGO',
    'ZONE1', 'ZONE2', 'MRG', 'REGULARITY', 'TOP_PACK', 'FREQ_TOP_PACK'
]

# Create label encoders for categorical features
label_encoders = {
    'REGION': LabelEncoder(),
    'TENURE': LabelEncoder(),
    'TOP_PACK': LabelEncoder()
}

# Example: Fit the encoders on your dataset
# You should fit them based on the entire dataset once, but for the example, let's assume values are already fit
label_encoders['REGION'].fit(['DAKAR', 'OTHER_REGION'])  # Add all possible regions
label_encoders['TENURE'].fit(['I 18-21 month', 'K > 24 month'])  # Add all tenure categories
label_encoders['TOP_PACK'].fit(["Data:1000F=5GB,7d", "On-net 1000F=10MilF;10d"])  # Add all top packs

# Get input from the user
st.subheader('Enter Customer Data:')
input_data = {}

for feature in feature_names:
    if feature in ['REGION', 'TENURE', 'TOP_PACK']:
        # Categorical input
        options = label_encoders[feature].classes_
        input_value = st.selectbox(f'Select {feature}:', options)
        input_data[feature] = label_encoders[feature].transform([input_value])[0]
    elif feature == 'user_id':
        input_data[feature] = st.text_input(f'Enter {feature}:')
    else:
        input_data[feature] = st.number_input(f'Enter {feature}:', step=0.01)

# Make a prediction
if st.button('Predict'):
    if model is not None:
        try:
            # Preprocess the input data
            input_df = pd.DataFrame([input_data])
            
            # Ensure all columns are in the correct data type and order
            input_df = input_df[feature_names]  # Ensure columns are in the same order as the model expects
            
            # Make the prediction
            prediction = model.predict(input_df)

            # Display the prediction
            st.write('Churn Prediction:', 'Yes' if prediction[0] == 1 else 'No')
        except Exception as e:
            st.error(f"An error occurred during prediction: {str(e)}")
    else:
        st.error("The model could not be loaded. Please check the 'svm_model.sav' file.")
