# Importing necessary libraries
import math
import numpy as np
import pickle
import streamlit as st

# Setting page wide configuration
st.set_page_config(page_title='IPL_Score_Predictor', layout="centered")

# Load the ML model
filename = 'ml_model.pkl'
model = pickle.load(open(filename, 'rb'))

# Title of the page with CSS
st.markdown("<h1 style='text-align: center; color: white;'> IPL Score Predictor 2022 </h1>", unsafe_allow_html=True)

# Add background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://4.bp.blogspot.com/-F6aZF5PMwBQ/Wrj5h204qxI/AAAAAAAABao/4QLn48RP3x0P8Ry0CcktxilJqRfv1IfcACLcBGAs/s1600/GURU%2BEDITZ%2Bbackground.jpg");
        background-attachment: fixed;
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Add description
with st.expander("Description"):
    st.info("""A Simple ML Model to predict IPL Scores between teams in an ongoing match. To make sure the model results accurate score and some reliability the minimum no. of current overs considered is greater than 5 overs.
    """)

# Select the batting team
batting_team = st.selectbox('Select the Batting Team ', ('Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab', 'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad'))

prediction_array = []

# Batting Team
teams = ['Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab', 'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad']
for team in teams:
    prediction_array.append(1 if team == batting_team else 0)

# Select the bowling team
bowling_team = st.selectbox('Select the Bowling Team ', ('Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab', 'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad'))

if bowling_team == batting_team:
    st.error('Bowling and Batting teams should be different')

# Bowling Team
for team in teams:
    prediction_array.append(1 if team == bowling_team else 0)

# Enter the current ongoing over
overs = st.number_input('Enter the Current Over', min_value=5.1, max_value=19.5, value=5.1, step=0.1)
if overs - math.floor(overs) > 0.5:
    st.error('Please enter a valid over input as one over only contains 6 balls')

# Enter current run
runs = st.number_input('Enter Current runs', min_value=0, max_value=354, step=1, format='%i')

# Wickets Taken till now
wickets = st.slider('Enter Wickets fallen till now', 0, 9, 0)

# Runs in last 5 over
runs_in_prev_5 = st.number_input('Runs scored in the last 5 overs', min_value=0, max_value=runs, step=1, format='%i')

# Wickets in last 5 over
wickets_in_prev_5 = st.number_input('Wickets taken in the last 5 overs', min_value=0, max_value=wickets, step=1, format='%i')

# Get all the data for predicting
prediction_array.extend([runs, wickets, overs, runs_in_prev_5, wickets_in_prev_5])
prediction_array = np.array([prediction_array])

if st.button('Predict Score'):
    # Call the ML Model
    prediction = model.predict(prediction_array)

    # Display the predicted Score Range
    predicted_score = int(round(prediction[0]))
    score_range = f'Predicted Match Score: {predicted_score - 5} to {predicted_score + 5}'
    st.success(score_range)
