import math
from utlis import *
import pandas as pd

# Prepare data for all analysis
# Baker game group is different between men and women
def getGameGroup(isWomen, row_no, game_type, num_baker_games, baker_match_distributions):
  if game_type == 'Team':
    return math.floor((row_no + 4) / 5)
  elif game_type == 'Baker':
    if isWomen:
      return math.floor((row_no + 4) / 5)
    else:
      return math.floor((row_no + 3) / 4)
    
  elif game_type == 'Baker Match Play':
    match_group = math.nan
    if row_no <= baker_match_distributions[0]:
      match_group = 1
    elif row_no <= np.sum(baker_match_distributions[0:2]):
      match_group = 2
    elif row_no <= np.sum(baker_match_distributions[0:3]):
      match_group = 3
    elif row_no <= np.sum(baker_match_distributions[0:4]):
        match_group = 4
    return match_group



# # Add columns - include strikes, double, spares, open
# def add_columns(df):
#     _df = df.copy()
#     _df['Strikes'] = _df.apply(lambda x: isStrike(x['First Ball']), axis=1)
#     _df['Spares'] = _df.apply(lambda x: isSpares(x['First Ball'], x['Second Ball']), axis=1)
#     _df['Opens'] = _df.apply(lambda x: isOpen(x['Frame No'], x['First Ball'], x['Second Ball']), axis=1)
#     _df['Doubles'] = _df.apply(lambda x: isDouble(x['Frame No'], _df.iloc[x.name - 1]['Strikes'], x['Strikes']), axis=1)
#     _df['Frame Score'] = _df.apply(lambda x: calcFrameScore(x.name, _df), axis=1)
#     return _df

def getCurrentFrameBowler(frame_no, data_row):
  if frame_no<=10:
    return data_row['Frame' + str(frame_no) + 'Ball1Bowler'].strip()
  elif frame_no == 11:
    return data_row['Frame10Ball2Bowler'].strip()
  elif frame_no == 12:
    return data_row['Frame10Ball3Bowler'].strip()
  else:
    return ''

def getCurrentFrameFirstBall(frame_no, data_row):
  if frame_no<=10:
    return data_row['Frame' + str(frame_no)+'Ball1']
  elif frame_no == 11:
    if data_row['Frame10Ball1'] == 10:
      return data_row['Frame10Ball2']
    elif data_row['Frame10Ball1'] + data_row['Frame10Ball2'] == 10:
      return data_row['Frame10Ball3']
  elif frame_no == 12:
    if data_row['Frame10Ball1'] == 10 and data_row['Frame10Ball2'] == 10:
      return data_row['Frame10Ball3']
    else:
      return 0
  else:
    return 0

def getCurrentFrameSecondBall(frame_no, data_row):
  if frame_no < 10:
    return data_row['Frame' + str(frame_no)+'Ball2']
  elif frame_no == 10:
    if data_row['Frame10Ball1'] == 10:
      return 0
    else: 
      return data_row['Frame10Ball2']
  elif frame_no == 11:
    if data_row['Frame10Ball1'] == 10 and data_row['Frame10Ball2'] == 10: 
      return 0
    elif data_row['Frame10Ball1'] == 10 and data_row['Frame10Ball2'] < 10:
      return data_row['Frame10Ball3']
    else:
      return 0
  else:
    return 0

def getPinLeave(frame_no, data_row):
  if frame_no<=10:
    return data_row['Frame' + str(frame_no)+'Ball1Pins']
  elif frame_no == 11:
    return data_row['Frame10Ball2Pins']
  elif frame_no == 12:
    return data_row['Frame10Ball3Pins']
  else: 
    return '-'

def getPin2Leave(frame_no, data_row):
  if frame_no<=10:
    return data_row['Frame' + str(frame_no)+'Ball2Pins']
  else:
    return '-'

def getFirstBallAttempt(frame_no, data_row):
  if frame_no <=10:
    return 1
  elif frame_no == 11:
    if data_row['Frame10Ball1'] == 10:
      return 1
    else: 
      return 0
  elif frame_no ==12:
    # if frame 11 is a strike
    if data_row['Frame10Ball2'] == 10:
      return 1
    # if frame 10 and frame 11 is finished
    elif data_row['Frame10Ball1'] + data_row['Frame10Ball2'] == 10:
      return 1
    else:
      return 0

def getIsSpare(frame_no, data_row):
  if frame_no <= 10:
    first_ball = data_row['Frame' + str(frame_no) + 'Ball1']
    second_ball = data_row['Frame' + str(frame_no) + 'Ball2']
    if second_ball == math.isnan:
      second_ball = 0
    if first_ball < 10 and first_ball + second_ball == 10:
      return 1
    else:
      return 0
  elif frame_no == 11: 
    # if frame 10 is a strike: frame 11 first ball will be Frame10Ball2 and second ball will be Frame10Ball3
    if data_row['Frame10Ball1'] == 10:
      first_ball = data_row['Frame10Ball2']
      second_ball = data_row['Frame10Ball3']
      if second_ball == math.isnan:
        second_ball = 0
      if first_ball < 10 and first_ball + second_ball == 10:
        return 1
      else:
        return 0
    # if frame 10 is not a strike, frame 11 first ball will be Frame10Ball3
    else:
      return 0
  else:
    return 0

def getIsStrike(frame_no, data_row):
  first_ball = 0
  if frame_no <=10:
    first_ball = data_row['Frame' + str(frame_no) + 'Ball1']
  elif frame_no == 11:
    if data_row['Frame10Ball1'] == 10:
      first_ball = data_row['Frame10Ball2']
    else:
      first_ball = data_row['Frame10Ball3']
  elif frame_no == 12:
    if data_row['Frame10Ball2'] == 10:
      first_ball = data_row['Frame10Ball3']
  if first_ball == 10:
    return 1
  else:
    return 0

def getIsDouble(game_type, frame_no, data_row):
  if game_type != 'Team':
    return '-'
  else:
    if frame_no == 1:
      return 0
    elif frame_no <=10:
      previous_ball1 = data_row['Frame' + str(frame_no - 1) + 'Ball1']
      current_ball1 = data_row['Frame' + str(frame_no) + 'Ball1']
      if previous_ball1 == 10 and current_ball1 == 10:
        return 1
      else:
        return 0
    elif frame_no == 11:
      previous_ball1 = data_row['Frame10Ball1']
      current_ball1 = data_row['Frame10Ball2']
      if previous_ball1 == 10 and current_ball1 == 10:
          return 1
      else:
          return 0
    elif frame_no == 12:
      previous_ball1 = data_row['Frame10Ball2']
      current_ball1 = data_row['Frame10Ball3']
      if previous_ball1 == 10 and current_ball1 == 10:
          return 1
      else:
          return 0
    else:
      return 0

def getIsDoubleAttempt(game_type, frame_no, data_row):
    if game_type != 'Team':
      return '-'
    else:
      if frame_no == 1:
        return 0
      elif frame_no <=10:
        previous_ball1 = data_row['Frame' + str(frame_no - 1) + 'Ball1']
        if previous_ball1 == 10:
          return 1
        else:
          return 0
      elif frame_no == 11:
        previous_ball1 = data_row['Frame10Ball1']
        if previous_ball1 == 10:
          return 1
        else:
          return 0
      elif frame_no == 12:
        previous_ball1 = data_row['Frame10Ball2']
     
        if previous_ball1 == 10:
          return 1
        else:
          return 0
      else:
        return 0
def getIsOpen(frame_no, data_row):
  first_ball = 0
  second_ball = 0
  if frame_no <=10:
    first_ball = data_row['Frame' + str(frame_no) + 'Ball1']
    second_ball = data_row['Frame' + str(frame_no) + 'Ball2']
    if second_ball is math.isnan:
      second_ball = 0
    if (first_ball+ second_ball <10):
      return 1
    else:
      return 0
  elif frame_no == 11:
    frame_10_ball = data_row['Frame10Ball1']
    frame_11_ball = data_row['Frame10Ball2']
    frame_12_ball = data_row['Frame10Ball3']
    if frame_12_ball is math.isnan:
      frame_12_ball = 0
    if frame_10_ball + frame_11_ball <10:
      return 0
    elif (frame_11_ball + frame_12_ball <10):
        return 1
    else:
      return 0
  elif frame_no == 12:
    return 0
def getAccumulatedScore(frame_no, data_row):
  if frame_no <=10:
    return data_row['Frame' + str(frame_no) + 'Score']
  else:
    return 0

def getCurrentFrameScore(frame_no, data_row):
  current_frame_score = 0
  previous_frame_score = 0
  if frame_no <=10:
    current_frame_score = data_row['Frame' + str(frame_no) + 'Score']
    if frame_no != 1:
      previous_frame_score = data_row['Frame' + str(frame_no - 1) + 'Score']
    return current_frame_score - previous_frame_score
  else:
    return 0

# Get every frame - gametype, match no, frame no, bowler, first ball, second ball, pin leave, pin leave 2
columns = [ 'game_type', 'game_group', 'game_no', 'frame_no',  'bowler', 'first_ball', 'second_ball', 'pin_leave', 'pin_leave_2', 'first_ball_attempt', 'spares', 'strikes', 'double', 'double_attempt', 'open','accumulated_score', 'frame_score']
def transform_to_frames(isWomen, _data, _game_type, num_baker_games, baker_match_distributions):
    data_entries = []
    _df = _data.copy()

    for row_no in range(len(_df)):
      game_no = row_no + 1
      current_row_data = _df.iloc[row_no]
      for i in range(12):
        frame_no = i + 1
        data_entry = [_game_type, getGameGroup(isWomen, game_no, _game_type, num_baker_games, baker_match_distributions), game_no , frame_no, getCurrentFrameBowler(frame_no,current_row_data ), getCurrentFrameFirstBall(frame_no, current_row_data) , getCurrentFrameSecondBall(frame_no, current_row_data), getPinLeave(frame_no, current_row_data), getPin2Leave(frame_no, current_row_data), getFirstBallAttempt(frame_no, current_row_data), getIsSpare(frame_no, current_row_data), getIsStrike(frame_no, current_row_data), getIsDouble(_game_type, frame_no, current_row_data), getIsDoubleAttempt(_game_type, frame_no, current_row_data), getIsOpen(frame_no, current_row_data), getAccumulatedScore(frame_no, current_row_data), getCurrentFrameScore(frame_no, current_row_data)]
        data_entries.append(data_entry)
    return pd.DataFrame(data_entries, columns=['game_type', 'game_group', 'game_no', 'frame_no', 'bowler', 'first_ball', 'second_ball', 'pin_leave', 'pin_2_leave', 'first_ball_attempt', 'spare', 'strike', 'double', 'double_attempt', 'open', 'accumulated_score', 'frame_score'])
