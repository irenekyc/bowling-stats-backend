import math
import numpy as np
import pandas as pd

# Calculate baker group no 
def groupBakerGame(match_no, total_game_group, total_bakers):
    num_of_matches_in_game = total_bakers / total_game_group
    return math.floor((match_no + (num_of_matches_in_game-1)) / num_of_matches_in_game)

def isStrike(first_ball):
    if first_ball == 10:
        return 1
    else:
        return 0
def isSpares(first_ball, second_ball):
    if first_ball < 10 and first_ball + second_ball == 10:
        return 1
    else:
        return 0
    
def hasFrame11(data):
    if math.isnan(data):
        return 0;
    else:
        return 1
    
def calcNumOfFirstBall(frame_11):
    if frame_11 == 1:
        return 11
    else:
        return 10
    
def isOpen(frame_no, first_ball, second_ball):
    if frame_no <=11:
        if first_ball == 10:
            return 0
        elif first_ball + second_ball >=10:
            return 0
        else:
            return 1
    else:
        return 0

        

def isDouble(frame_no, previous_strikes, current_strikes):
    if frame_no == 1:
        return 0
    else:
        if previous_strikes == 1 and current_strikes == 1:
            return 1
        else:
            return 0

    
def calcStrikesPercentageWithNumber(num_of_strikes, total_first_ball):
    if total_first_ball == 0:
        return 0
    else:
        return str(round(num_of_strikes/total_first_ball * 100, 2)) +'%'

def convertAverageToPercentage(average):
    return str(round(average* 100, 2)) +'%'

game_type_column_name = 'GameType'
first_baker_no = 25

def transformBakerGameType(x):
    if x.name <= first_baker_no:
        return 'Baker'
    else:
        return 'Baker Match Play'

def getTeamNo(i):
    return math.floor((i+5)/5)

def isDoubleAttempt(frame_no, row_data):
    previous_first_ball = 0
    if frame_no == 11:
        previous_first_ball = row_data['Frame10Ball1']
    if frame_no == 12:
        previous_first_ball = row_data['Frame10Ball2'] 
    elif frame_no !=1 :
        previous_first_ball = row_data['Frame' + str(frame_no - 1) + 'Ball1']
    
    if previous_first_ball == 10:
        return 1
    else: 
        return 0

def isFirstBallAttempt(frame_no, previous_ball, previous_2_ball):
    # every 1st - 9th frame has a first ball
    if frame_no == 11:
        if (previous_ball == 10):
            return 1
        else: 
            return 0
    # if it is frame 11, check if frame 10 is strike
    # if it is frame 12, check if frame 11 is a strike OR frame 10 + frame 11 = 10
    elif frame_no == 12:
        if (previous_ball == 10 or previous_ball + previous_2_ball == 10):
            return 1;
        else:
            return 0;
    else:
        return 1

def calcFrameScore(i, _df):
    frame_no = _df['Frame No'].iloc[i]
    current_score = _df['Score'].iloc[i]
    if i == 0 or frame_no == 1:
        return     current_score 
    else:
        previous_score = _df['Score'].iloc[i-1]
        return current_score - previous_score


def addMetaData(df, team_name, event_name, year, event_id, location, start_date, end_date):

    original_columns = df.columns
    _df = df.copy()
    _df['Team Name'] = team_name
    _df['Event Name'] = event_name
    _df['Year'] = year
    _df['Event Id'] = event_id
    _df['Location'] = location
    _df['start_date'] = start_date
    _df['end_date'] = end_date
    new_columns = np.concatenate((['Event Id', 'Team Name', 'Event Name', 'Year', 'Location', 'start_date', 'end_date'],original_columns), axis=None)
    _df = _df.reindex(columns=new_columns)
    return _df

def getEventName(df):
    event_name = _df['Location'].unique()
    location = [value for value in location if isinstance(value, str)]

    return ' , '.join(location)

def getEventLocation(df):
    _df = df.copy()
    
    location = _df['Location'].unique()
    location = [value for value in location if isinstance(value, str)]

    return ' , '.join(location)

def getEventDate(df):
    _df = df.copy()    
    _df['Date - Pandas'] = pd.to_datetime(_df['Date'])
    _df['Date - Date'] = _df['Date - Pandas'].dt.date
    date = _df['Date - Date'].dropna().unique()

    start_date = min(date)
    end_date = max(date)

    return (start_date, end_date)
    # start_date = _df['Location'].unique()
    # location = [value for value in location if isinstance(value, str)]