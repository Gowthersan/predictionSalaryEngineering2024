import pickle

import numpy as np
import streamlit as st


# Load the trained model
def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


data = load_model()


regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]


# Define the user interface
def show_predict_page():
    """
    Display the software engineer salary prediction app.
    """
    st.title("Software Engineer Salary Prediction App")

    st.write("""### We need some information to predict the salary""")
    

    countries = (
        "United States of America",
        "India",
        "United Kingdom of Great Britain and Northern Ireland",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Ukraine"
    )

    education_level = (
        "Less than a Bachelors",
        "Bachelor's degree",
        "Master's degree",
        "Post grad",
    )

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education_level)

    experience = st.slider("Years of Experience", 0, 50, 3)
    
    ok = st.button("Predict Salary")
    if ok:
        X = np.array([[country, education, experience]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)
        
        salary = regressor.predict(X)
        
        st.subheader(f"Salary Estimated is : ${salary[0]:.2f}")