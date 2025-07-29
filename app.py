import streamlit as st
import pickle
import pandas as pd

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



st.title("IPL Match Winning Predictor")



teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
       'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Sharjah', 'Mohali', 'Bengaluru']

pipe = pickle.load(open('pipe.pkl','rb'))

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team',sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team',sorted(teams))

selected_city = st.selectbox('Select host city',sorted(cities))

target = st.number_input('Target')

col3,col4,col5 = st.columns(3)

with col3:
    score = st.number_input('Current Score',min_value=0)
with col4:
    overs = st.number_input('Overs completed',min_value=0.0,max_value=20.0,format='%.1f')
with col5:
    wickets = st.number_input('Wickets Lost',min_value=0,max_value=10)

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - int(overs*6)
    wickets = 10 - wickets

    if overs == 0 or balls_left <= 0:
        st.warning("Match has not started yet. Please enter at least 1 over. ")
    else:
        try:
            crr= score/overs
            rrr = (runs_left*6)/balls_left

            input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets':[wickets],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})

            result = pipe.predict_proba(input_df)
            loss = result[0][0]
            win = result[0][1]

            st.success(f"{batting_team}Winning Probability: **{round(win*100)}%**")
            st.info(f"{bowling_team}Winning Probability: **{round(loss*100)}%**")
        except ZeroDivisionError:
            st.error("Cannot compute probabilities due to zero overs or balls.")
        except Exception as e:
            st.error(f"Error: {e}")