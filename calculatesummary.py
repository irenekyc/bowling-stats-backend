import pandas as pd
from columns import event_summary_excel_columns

def calculatesummarydata(df):
  _df = df.copy()
  _df_all = _df
  _df_baker = _df[_df['game_type'] == 'Baker']
  _df_team = _df[_df['game_type'] == 'Team']
  _df_baker_mp = _df[_df['game_type'] == 'Baker Match Play']

  _df_baker = _df_baker.groupby(['bowler']).agg(baker_num_frames=('first_balls', 'sum'), baker_frame_ave=('frame_average', 'mean'), baker_num_strikes=('num_strikes', 'sum'), baker_num_strikes_attempt=('first_balls', 'sum'), baker_strikes_percentage=('strikes_percentage', 'mean'), baker_first_ball_ave=('first_ball_ave', 'mean')).reset_index().set_index('bowler')
  _df_team = _df_team.groupby(['bowler']).agg(team_num_frames=('first_balls', 'sum'), team_frame_ave=('frame_average', 'mean'), team_num_strikes=('num_strikes', 'sum'), team_num_strikes_attempt=('first_balls', 'sum'), team_strikes_percentage=('strikes_percentage', 'mean'), team_first_ball_ave=('first_ball_ave', 'mean'), team_doubles=('num_doubles', 'sum'), team_doubles_attempt=('num_double_attempts', 'sum'), team_double_percentage=('double_percentage', 'mean')).reset_index().set_index('bowler')
  _df_baker_mp = _df_baker_mp.groupby(['bowler']).agg(baker_mp_num_frames=('first_balls', 'sum'),baker_mp_frame_ave=('frame_average', 'mean'),baker_mp_num_strikes=('num_strikes', 'sum'), baker_mp_num_strikes_attempt=('first_balls', 'sum'), baker_mp_strikes_percentage=('strikes_percentage', 'mean'), baker_mp_first_ball_ave=('first_ball_ave', 'mean')).reset_index().set_index('bowler')
  _df_all = _df_all.groupby(['bowler']).agg(all_num_frames=('first_balls', 'sum'),all_frame_ave=('frame_average', 'mean'),all_num_strikes=('num_strikes', 'sum'), all_num_strikes_attempt=('first_balls', 'sum'), all_strikes_percentage=('strikes_percentage', 'mean'), all_first_ball_ave=('first_ball_ave', 'mean')).reset_index().set_index('bowler')


  _df_combine = pd.concat([_df_baker, _df_team, _df_baker_mp,_df_all], axis=1).reset_index()
  
  return _df_combine 