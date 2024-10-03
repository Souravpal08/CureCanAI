import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Inject custom CSS to make the width 100%
def set_max_width():
    max_width_str = """
    <style>
    .main {
        max-width: 100%;
        padding-left: 5%;
        padding-right: 5%;
    }
    </style>
    """
    st.markdown(max_width_str, unsafe_allow_html=True)

# Load the model, scaler, and feature names
def load_model():
    model = joblib.load('model/model.pkl')
    scaler = joblib.load('model/scaler.pkl')
    feature_names = joblib.load('model/feature_names.pkl')
    return model, scaler, feature_names

# Input section
def get_user_input():
    st.header('Input Features')

    # Create input sliders for all features used in training
    radius_mean = st.slider('Radius Mean', 0.0, 30.0, 14.0)
    texture_mean = st.slider('Texture Mean', 0.0, 40.0, 19.0)
    perimeter_mean = st.slider('Perimeter Mean', 0.0, 200.0, 90.0)
    area_mean = st.slider('Area Mean', 0.0, 2500.0, 700.0)
    smoothness_mean = st.slider('Smoothness Mean', 0.0, 0.2, 0.1)
    compactness_mean = st.slider('Compactness Mean', 0.0, 1.0, 0.2)
    concavity_mean = st.slider('Concavity Mean', 0.0, 1.0, 0.3)
    concave_points_mean = st.slider('Concave Points Mean', 0.0, 1.0, 0.2)
    symmetry_mean = st.slider('Symmetry Mean', 0.0, 1.0, 0.2)
    fractal_dimension_mean = st.slider('Fractal Dimension Mean', 0.0, 0.1, 0.05)

    # Ensure all necessary features are captured (missing ones included)
    radius_se = st.slider('Radius SE', 0.0, 5.0, 1.0)
    texture_se = st.slider('Texture SE', 0.0, 5.0, 1.0)

    # Collect all inputs into a dictionary
    user_data = {
        'radius_mean': radius_mean,
        'texture_mean': texture_mean,
        'perimeter_mean': perimeter_mean,
        'area_mean': area_mean,
        'smoothness_mean': smoothness_mean,
        'compactness_mean': compactness_mean,
        'concavity_mean': concavity_mean,
        'concave points_mean': concave_points_mean,
        'symmetry_mean': symmetry_mean,
        'fractal_dimension_mean': fractal_dimension_mean,
        'radius_se': radius_se,
        'texture_se': texture_se,
    }

    # Convert the dictionary into a DataFrame for later processing
    features = pd.DataFrame(user_data, index=[0])
    return features

# Main function
def main():
    set_max_width()  # Apply custom width

    st.title("Breast Cancer Detection")

    # Create two columns: One for the inputs and one for the output
    col1, col2 = st.columns([1, 1.5])

    # Load the model, scaler, and feature names
    model, scaler, feature_names = load_model()

    with col1:
        # Get user input
        user_input = get_user_input()

    with col2:
        # Add some space between the input section and the prediction section
        st.markdown("<br><br><br>", unsafe_allow_html=True)

        # Ensure the input data matches the expected feature set
        for feature in feature_names:
            if feature not in user_input.columns:
                user_input[feature] = 0  # Assign default value to missing features

        # Reorder columns to match the order of features used during training
        user_input = user_input[feature_names]

        # Standardize the user input before prediction
        user_input_scaled = scaler.transform(user_input)

        # Predict button
        if st.button('Predict'):
            # Predict the class (Benign or Malignant)
            prediction = model.predict(user_input_scaled)
            prediction_prob = model.predict_proba(user_input_scaled)[0]

            # Display the prediction result
            if prediction == 1:
                st.markdown("<h2 style='color: red;'>The prediction is: Malignant</h2>", unsafe_allow_html=True)
                st.markdown("""
                <div style='background-color: #f8d7da; padding: 10px; border-radius: 5px; color: black;'>
                    <p><strong>Description:</strong> The model predicts that the tumor is <strong>malignant</strong>. Malignant tumors are cancerous, meaning they can grow and spread to other parts of the body.</p>
                    <p>It's recommended that you consult with a healthcare professional for further tests and advice. Early detection and treatment are crucial in managing breast cancer effectively.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("<h2 style='color: green;'>The prediction is: Benign</h2>", unsafe_allow_html=True)
                st.markdown("""
                <div style='background-color: #d4edda; padding: 10px; border-radius: 5px; color: black;'>
                    <p><strong>Description:</strong> The model predicts that the tumor is <strong>benign</strong>. Benign tumors are non-cancerous and generally do not spread to other parts of the body.</p>
                    <p>While benign tumors are less harmful than malignant ones, it's still advisable to monitor them and consult with a doctor.</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Display prediction probabilities as a pie chart
            display_chart(prediction_prob)

# Function to display prediction probabilities as a pie chart
def display_chart(probabilities):
    labels = ['Benign', 'Malignant']
    fig, ax = plt.subplots()
    ax.pie(probabilities, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#8fbc8f', '#f08080'])
    ax.axis('equal')  # Ensure the pie chart is circular
    st.pyplot(fig)

main()
