
import streamlit as st
import pandas as pd
import joblib

# Set page configuration
st.set_page_config(
    page_title="Student Performance Prediction App",
    page_icon="🎓",
    layout="wide",
)

# Inject CSS for styling the input fields' width
def inject_css():
    st.markdown(
        """
        <style>
        .stNumberInput > div > input {
            max-width: 500px;  /* Adjust this value to set the max width of the number input fields */
        }
        .stTextInput > div > input {
            max-width: 100px;  /* Adjust this value to set the max width of the text input fields */
        }
        </style>
        """, unsafe_allow_html=True
    )

# Call the function to inject CSS
inject_css()



# Load saved pipeline (includes both preprocessor and model)
@st.cache_resource
def load_pipeline():
    pipeline = joblib.load('hackathon_pipeline.pkl')  # Assuming your preprocessor and model are saved in one pipeline
    return pipeline

pipeline = load_pipeline()

# Mapping of full feature names to abbreviated names
feature_mapping = {
    'Internet Availability': 'Internet Availability',
    'Access to Textbooks': 'Access to Textbooks',
    'Attendance Rate': 'Attendance Rate',
    'Class Participation Score': 'Class Participation Score',
    'Homework Completion Rate': 'Homework Completion Rate',
    'Hours Spent on Self-study': 'Hours Spent on Self-study',
    'Type of Activity': 'Type of Activity',
    'Hours per Week': 'Hours per Week',
    'Parental Education Level': 'Parental Education Level',
    'Household Income': 'Household Income',
    'Number of Siblings': 'Number of Siblings',
    'Library Hours Used': 'Library Hours Used',
    'Teacher-to-student Ratio': 'Teacher-to-student Ratio',
    'Access to Study Materials': 'Access to Study Materials',
    'Extra Tutoring Hours': 'Extra Tutoring Hours',
    'Age': 'Age',
    'Gender': 'Gender',
    'Subject Combinations': 'Subject Combinations'
}

predefined_samples = {
    "Sample 1": {
        'Internet Availability': 'Yes', 'Access to Textbooks': 'Yes', 'Attendance Rate': 83, 'Class Participation Score': 76, 
        'Homework Completion Rate': 87, 'Hours Spent on Self-study': 5, 'Type of Activity': 'Music', 'Hours per Week': 1, 
        'Parental Education Level': 'Secondary', 'Household Income': 141851, 'Number of Siblings': 0, 'Library Hours Used': 4, 
        'Teacher-to-student Ratio': 25, 'Access to Study Materials': 'Yes', 'Extra Tutoring Hours': 0, 'Age': 24, 
        'Gender': 'Male', 'Subject Combinations': 'Theoretical Arts'
    },
    "Sample 2": {
        'Internet Availability': 'Yes', 'Access to Textbooks': 'Yes', 'Attendance Rate': 80, 'Class Participation Score': 63, 
        'Homework Completion Rate': 69, 'Hours Spent on Self-study': 9, 'Type of Activity': 'Sports', 'Hours per Week': 11, 
        'Parental Education Level': 'Primary', 'Household Income': 209440, 'Number of Siblings': 0, 'Library Hours Used': 9, 
        'Teacher-to-student Ratio': 25, 'Access to Study Materials': 'Yes', 'Extra Tutoring Hours': 3, 'Age': 23, 
        'Gender': 'Male', 'Subject Combinations': 'Applied commerce'
    }
}

# Sidebar for predefined sample selection
st.sidebar.title("Settings")
selected_sample_name = st.sidebar.selectbox(
    "Select a Sample",
    options=[None] + list(predefined_samples.keys())
)

# Get the selected sample
selected_sample = predefined_samples.get(selected_sample_name, {})

# Main content
st.title("🎓 Providus College")

st.header("Enter Input Values")

# Create two columns for input fields
col1, col2 = st.columns(2)

# Create input fields for all features using full names
user_input = {}
with col1:
    st.subheader("Features - Part 1")
    for i, (full_name, short_name) in enumerate(feature_mapping.items()):
        if i < len(feature_mapping) // 2:  # First half of features
            value = selected_sample.get(short_name, "")
            if isinstance(value, int):
                # Use text_input for integers to remove + and - adjustments
                user_input[short_name] = st.text_input(f"{full_name}:", value=str(value))
            else:
                user_input[short_name] = st.text_input(f"{full_name}:", value=str(value))

with col2:
    st.subheader("Features - Part 2")
    for i, (full_name, short_name) in enumerate(feature_mapping.items()):
        if i >= len(feature_mapping) // 2:  # Second half of features
            value = selected_sample.get(short_name, "")
            if isinstance(value, int):
                # Use text_input for integers to remove + and - adjustments
                user_input[short_name] = st.text_input(f"{full_name}:", value=str(value))
            else:
                user_input[short_name] = st.text_input(f"{full_name}:", value=str(value))

if st.button("Predict"):
    # Ensure the DataFrame columns match the feature names used during training
    input_df = pd.DataFrame([user_input])

    # Prediction using the pipeline
    prediction = pipeline.predict(input_df)
    
    # Display Results
    st.subheader("Prediction Result")
    st.write(f"The model predicts: **{prediction[0]}**")


