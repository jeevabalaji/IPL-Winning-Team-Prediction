import streamlit as st
import pandas as pd
import pickle

teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
         'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
         'Rajasthan Royals', 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
          'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah', 'Mohali', 'Bengaluru']

pipe = pickle.load(open('pipe.pkl', 'rb'))

st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    battingteam = st.selectbox('Select the batting team', sorted(teams))

with col2:
    bowlingteam = st.selectbox('Select the bowling team', sorted(teams))

city = st.selectbox('Select the city where the match is being played', sorted(cities))

target = int(st.number_input('Target', step=1))

col3, col4, col5 = st.columns(3)

with col3:
    score = int(st.number_input('Score', step=1))

with col4:
    overs = int(st.number_input('Overs Completed', step=1))

with col5:
    wickets = int(st.number_input('Wickets Fallen', step=1))

if score > target:
    st.write(battingteam, "won the match")
    
elif score == target - 1 and overs == 20:
    st.write("Match Drawn")
    
elif wickets == 10 and score < target - 1:
    st.write(bowlingteam, 'Won the match')
    
elif wickets == 10 and score == target - 1:
    st.write('Match tied')
    
elif battingteam == bowlingteam:
    st.write('To proceed, please select different teams because no match can be played between the same teams')

else:
    if 0 <= target <= 300 and 0 <= overs <= 20 and 0 <= wickets <= 10 and score >= 0:
        try:
            if st.button('Predict Probability'):
                runs_left = target - score 
                balls_left = 120 - (overs * 6)
                wickets_left = 10 - wickets
                current_run_rate = score / overs if overs > 0 else 0
                required_run_rate = (runs_left * 6) / balls_left if balls_left > 0 else 0
                               
                input_df = pd.DataFrame(
                               {'batting_team': [battingteam], 
                                'bowling_team': [bowlingteam], 
                                'city': [city], 
                                'runs_left': [runs_left], 
                                'balls_left': [balls_left],
                                'wickets_left': [wickets_left],
                                'total_runs_x': [target], 
                                'cur_run_rate': [current_run_rate], 
                                'req_run_rate': [required_run_rate]})
                
                result = pipe.predict_proba(input_df)
                
                loss_prob = result[0][0]
                win_prob = result[0][1]
                
                st.header(battingteam + " - " + str(round(win_prob * 100)) + "%")
                st.header(bowlingteam + " - " + str(round(loss_prob * 100)) + "%")
                
        except ZeroDivisionError:
            st.error("Please fill all the details")
            
    else:
        st.error('There is something wrong with the input, please fill in the correct details')
