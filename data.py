import pandas as pd 
import json
from csvtransform import *
from transformtotable import *
from datamen import analysisBowlingDataMen
import os

def analysisBowlingDataChampionships(team_name, filePath, event_name, location, year, match_game_pattern, baker_match_play_distribution):
  df = pd.read_csv(filePath, index_col=False)
  df =  df.drop(columns="Event")
  df =  df.drop(columns="EventType")
  event_id = event_name.replace(" ", "-").lower() + "--"+ year.replace(" ", "")
  (start_date, end_date)= getEventDate(df)
  is_women = True
  if team_name == 'QU Women':
    is_women = True
  else: 
    is_women = False

  _starting_game_entry = 1
  _analyized_data_arr = []
  _summary_data_arr = []

  for index, match_game in enumerate(match_game_pattern):
    _df = pd.DataFrame()
    _df_data_arr = []
    current_baker_mp_distribution = baker_match_play_distribution[index]
    for game_type in match_game:
      _df_data_set = df.iloc[_starting_game_entry : _starting_game_entry + match_game[game_type]]
      _starting_game_entry = _starting_game_entry + match_game[game_type]
      _df_data_set['GameType'] = game_type
      _df_data_arr.append(_df_data_set)
    
    _df = pd.concat(_df_data_arr, axis=0)
    _df_team = _df[_df['GameType'] == 'Team']
    _df_baker = _df[_df['GameType'] == 'Baker']
    _df_baker_match = _df[_df['GameType'] == 'Baker Match Play']
      

    # 2. Transform csv table into 12 frames format  
    team_data = transform_to_frames(is_women, _df_team, 'Team', match_game["Baker"] / 5, current_baker_mp_distribution)
    team_data['game_group'] = index + 1
    baker_data = transform_to_frames(is_women,_df_baker, 'Baker', match_game["Baker"] / 5, current_baker_mp_distribution)
    baker_data['game_group'] = index + 1
    baker_match_data= transform_to_frames(is_women,_df_baker_match, 'Baker Match Play', match_game["Baker"] / 5, current_baker_mp_distribution)


    # # 3. Analyize data
    (analysized_data, summary_data) = transform_to_table([baker_data, team_data, baker_match_data], 5)
    _analyized_data_arr.append(analysized_data)
    _summary_data_arr.append(summary_data)

  analysized_data_all = pd.concat(_analyized_data_arr, axis=0)
  summary_data_all = pd.concat(_summary_data_arr, axis=0)
  analysized_data_all = addMetaData(analysized_data_all, team_name, event_name, year, event_id, location, start_date, end_date)
  summary_data_all = addMetaData(summary_data_all, team_name, event_name, year, event_id, location, start_date, end_date)
  
  output_dir = ''
  if team_name == 'QU Women':
    output_dir = './excels-women/raw-events/'
  else:
    output_dir = './excels-men/raw-events/'

  output_dir_summary = ''
  if team_name == 'QU Women':
    output_dir_summary = './excels-women/raw-events-summary/'
  else:
    output_dir_summary = './excels-men/raw-events-summary/'

  analysized_data_all.to_excel('{output_dir}{team_name}-{event}.xlsx'.format(team_name=team_name, event=event_name, output_dir=output_dir), sheet_name=event_id, index=False)
  summary_data_all.to_excel('{output_dir_summary}{team_name}-{event}-summary.xlsx'.format(team_name=team_name, event=event_name, output_dir_summary=output_dir_summary), sheet_name='summary', index=False)

def analysisBowlingData(team_name, filePath, event_name, location, year, num_of_baker_games, baker_match_play_distributions):
  df = pd.read_csv(filePath, index_col=False)
  df =  df.drop(columns="Event")
  df =  df.drop(columns="EventType")
  (start_date, end_date)= getEventDate(df)

  columns_name = df.columns
  event_id = event_name.replace(" ", "-").lower() + "--"+ year.replace(" ", "")
  is_women = True
  if team_name == 'QU Women':
    is_women = True
  else: 
    is_women = False

  # 1. Divided into Baker, Baker Match and Baker 
  _df_team = df[df['GameType'] == 'Team']
  _df_baker = df[df['GameType'] == 'Baker'].iloc[0: 5*num_of_baker_games]
  _df_baker_match = pd.DataFrame()
  _df_baker_match = df[df['GameType'] == 'Baker'].iloc[5*num_of_baker_games:]
  _df_baker_match['GameType'] = 'Baker Match Play'
  

  # 2. Transform csv table into 12 frames format  
  team_data = transform_to_frames(isWomen=is_women, _data=_df_team, _game_type='Team', num_baker_games=num_of_baker_games, baker_match_distributions=baker_match_play_distributions)
  baker_data = transform_to_frames(isWomen=is_women, _data=_df_baker, _game_type='Baker', num_baker_games=num_of_baker_games, baker_match_distributions=baker_match_play_distributions)
  baker_match_data= transform_to_frames(isWomen=is_women, _data=_df_baker_match, _game_type='Baker Match Play',num_baker_games=num_of_baker_games, baker_match_distributions=baker_match_play_distributions)


  # 3. Analyize data
  (analysized_data, summary_data) = transform_to_table([baker_data, team_data, baker_match_data], 5)
  analysized_data = addMetaData(analysized_data, team_name, event_name, year, event_id, location, start_date, end_date)
  summary_data = addMetaData(summary_data, team_name, event_name, year, event_id, location, start_date, end_date)
  analysized_data.to_excel('checking.xlsx'.format(team_name=team_name, event=event_name), sheet_name=event_id)

  output_dir = ''
  output_dir_summary = ''
  if is_women:
    output_dir = './excels-women/raw-events/'
    output_dir_summary = './excels-women/raw-events-summary/'
  else:
    output_dir = './excels-men/raw-events/'
    output_dir_summary = './excels-men/raw-events-summary/'


  
  analysized_data.to_excel('{output_dir}{team_name}-{event}.xlsx'.format(team_name=team_name, event=event_name, output_dir=output_dir), sheet_name=event_id, index=False)
  summary_data.to_excel('{output_dir_summary}{team_name}-{event}-summary.xlsx'.format(team_name=team_name, event=event_name, output_dir_summary=output_dir_summary), sheet_name='summary', index=False)
  #TODO: add to database


# QU Women
# get all files from directory
women_files_dir = './raw-csv/qu-women/'
team_name = 'QU Women'

analysisBowlingData(team_name=team_name, filePath=women_files_dir + 'QU Women 2021-2022 (7).csv' , event_name='Big Red Invite', location='Hollywood Bowl', year='2021 - 2022', num_of_baker_games=5, baker_match_play_distributions=[7,5])
analysisBowlingData(team_name=team_name, filePath=women_files_dir + 'QU Women 2021-2022 (4) - Peacocks Classic.csv' , event_name='Peacocks Classic', location='Cadillac XBC', year='2021 - 2022', num_of_baker_games=5, baker_match_play_distributions=[4,6])
analysisBowlingData(team_name=team_name, filePath=women_files_dir + 'QU Women 2021-2022 (6) - Flyer Classic.csv' , event_name='Flyer Classic', location='Strike And Spare II', year='2021 - 2022', num_of_baker_games=5, baker_match_play_distributions=[4,6,7])
analysisBowlingData(team_name=team_name, filePath=women_files_dir + 'Bearcat Open.csv' , event_name='Bearcat Open', location='St Clair Bowl', year='2021 - 2022', num_of_baker_games=5, baker_match_play_distributions=[7,4,6])
analysisBowlingData(team_name=team_name, filePath=women_files_dir + 'Warhawk Open.csv' , event_name='Warhawk Open', location='Rock River Lanes, North rock Lanes', year='2021 - 2022', num_of_baker_games=5, baker_match_play_distributions=[])
analysisBowlingDataChampionships(team_name=team_name, filePath=women_files_dir + 'GLVC Championships.csv' , event_name='GLVC Championships', location='Bowlero Lakeside', year='2021 - 2022', match_game_pattern=[{ "Team": 5, "Baker": 5, "Baker Match Play": 0}, { "Team": 5, "Baker": 5, "Baker Match Play": 0}, { "Team": 5, "Baker": 5, "Baker Match Play": 0}], baker_match_play_distribution=[[], [], []])

men_files_dir = './raw-csv/qu-men/'


analysisBowlingData(team_name='QU Men', filePath=men_files_dir + 'QU Men - Five Seasons Classic.csv',  event_name='Five Seasons Classic', location= 'May City Bowl', year='2021 - 2022', num_of_baker_games=4, baker_match_play_distributions=[])
analysisBowlingData(team_name='QU Men', filePath=men_files_dir +'QU Men - Kegel-ISBPA Midwest Classic.csv',   event_name='Kegel-ISBPA Midwest Classic', location='Stardust Bowl', year='2021 - 2022', num_of_baker_games=5,baker_match_play_distributions=[])
analysisBowlingData(team_name='QU Men', filePath=men_files_dir +'QU Men - Kohawk Invite.csv',  event_name='Kohawk Invite', location='Cedar Rapids Bowling Center', year='2021 - 2022',  num_of_baker_games=4, baker_match_play_distributions=[])
analysisBowlingData(team_name='QU Men', filePath=men_files_dir +'QU Men - Leatherneck Classic.csv',  event_name='Leatherneck Classic', location='Big River Bowl', year='2021 - 2022', num_of_baker_games=4, baker_match_play_distributions=[])
analysisBowlingData(team_name='QU Men', filePath=men_files_dir + 'QU Men - Mid States Championships.csv', event_name= 'Mid States Championships',location='North rock Lanes', year= '2021 - 2022', num_of_baker_games=5,baker_match_play_distributions=[])