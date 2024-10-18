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

# Sidebar for predefined sample selection
st.sidebar.title("Settings")
selected_sample_name = st.sidebar.selectbox(
    "Select a Sample",
    options=[None] + ['Sample 1', 'Sample 2']
)

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
    st.subheader("Part 1")
    user_input['Internet Availability'] = st.selectbox(
        "Internet Availability:", ['Yes', 'No'], index=0 if selected_sample.get('Internet Availability') == 'Yes' else 1)
    user_input['Access to Textbooks'] = st.selectbox(
        "Access to Textbooks:", ['Yes', 'No'], index=0 if selected_sample.get('Access to Textbooks') == 'Yes' else 1)
    user_input['Attendance Rate'] = st.text_input(
        "Attendance Rate (0-100):", value=str(selected_sample.get('Attendance Rate', '')))
    user_input['Class Participation Score'] = st.text_input(
        "Class Participation Score (0-100):", value=str(selected_sample.get('Class Participation Score', '')))
    user_input['Homework Completion Rate'] = st.text_input(
        "Homework Completion Rate (0-100):", value=str(selected_sample.get('Homework Completion Rate', '')))
    user_input['Hours Spent on Self-study'] = st.text_input(
        "Hours Spent on Self-study (0-20):", value=str(selected_sample.get('Hours Spent on Self-study', '')))
    user_input['Type of Activity'] = st.selectbox(
        "Type of Activity:", ['Music', 'Science Club', 'Drama', 'Sports'], index=['Music', 'Science Club', 'Drama', 'Sports'].index(selected_sample.get('Type of Activity', 'Music')))
    user_input['Hours per Week'] = st.text_input(
        "Hours per Week (0-15):", value=str(selected_sample.get('Hours per Week', '')))
    user_input['Extra Tutoring Hours'] = st.text_input(
        "Extra Tutoring Hours (0-5):", value=str(selected_sample.get('Extra Tutoring Hours', '')))

with col2:
    st.subheader("Part 2")
    user_input['Library Hours Used'] = st.text_input(
        "Library Hours Used (0-10):", value=str(selected_sample.get('Library Hours Used', '')))
    user_input['Parental Education Level'] = st.selectbox(
        "Parental Education Level:", ['Secondary', 'Primary', 'Tertiary'], index=['Secondary', 'Primary', 'Tertiary'].index(selected_sample.get('Parental Education Level', 'Secondary')))
    user_input['Access to Study Materials'] = st.selectbox(
        "Access to Study Materials:", ['Yes', 'No'], index=0 if selected_sample.get('Access to Study Materials') == 'Yes' else 1)
    user_input['Gender'] = st.selectbox(
        "Gender:", ['Male', 'Female'], index=0 if selected_sample.get('Gender') == 'Male' else 1)
    user_input['Subject Combinations'] = st.selectbox(
        "Subject Combinations:", ['Applied commerce', 'Pure science', 'Theoretical Arts', 'Applied Arts', 'Theoretical commerce', 'Biological Science', 'Applied science'], 
        index=['Applied commerce', 'Pure science', 'Theoretical Arts', 'Applied Arts', 'Theoretical commerce', 'Biological Science', 'Applied science'].index(selected_sample.get('Subject Combinations', 'Applied commerce')))
    
    # Fields without limits
    user_input['Teacher-to-student Ratio'] = st.text_input(
        "Teacher-to-student Ratio:", value=str(selected_sample.get('Teacher-to-student Ratio', '')))
    user_input['Age'] = st.text_input(
        "Age:", value=str(selected_sample.get('Age', '')))
    user_input['Number of Siblings'] = st.text_input(
        "Number of Siblings:", value=str(selected_sample.get('Number of Siblings', '')))
    user_input['Household Income'] = st.text_input(
        "Household Income:", value=str(selected_sample.get('Household Income', '')))

if st.button("Predict"):
    # Ensure the DataFrame columns match the feature names used during training
    input_df = pd.DataFrame([user_input])

    # Prediction using the pipeline
    prediction = pipeline.predict(input_df)
    
    # Display Results
    st.subheader("Prediction Result")
    st.write(f"The model predicts: **{prediction[0]}**")
