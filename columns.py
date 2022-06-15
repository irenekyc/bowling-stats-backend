# transformed excel
transformed_excel_columns = [ 'game_type', 'game_group', 'game_no', 'frame_no',  'bowler', 'first_ball', 'second_ball', 'pin_leave', 'pin_leave_2', 'first_ball_attempt', 'spares', 'strikes', 'double', 'double_attempt', 'opens','accumulated_score', 'frame_score']

# output excel
output_excel_columns=['game_type', 'game_group', 'game_no', 'frame_no',  'bowler', 'num_frames',  'first_ball', 'first_ball_attempt', 'first_ball_average', 'spares', 'spares_per_game', 'strikes', 'strikes_percentage','strikes_per_game', 'double', 'double_attempt', 'double_percentage','opens', 'opens_per_game', 'frame_average']

# event summary excel
event_summary_excel_columns = ["bowler", 
'baker_num_frames', 'baker_frame_ave', 'baker_num_strikes','baker_num_strikes_attempt','baker_strikes_percentage' , 'baker_first_ball_ave',
'team_num_frames', 'team_frame_ave', 'team_num_strikes','team_num_strikes_attempt', 'team_strikes_percentage',  'team_first_ball_ave', 'team_doubles', 'team_doubles_attempt', 'team_double_percentage',
'baker_mp_num_frames', 'baker_mp_frame_ave', 'baker_mp_num_strikes','baker_mp_num_strikes_attempt','baker_mp_strikes_percentage' , 'baker_mp_first_ball_ave',
'all_num_frames', 'all_frame_ave', 'all_num_strikes','all_num_strikes_attempt', 'all_strikes_percentage',  'all_first_ball_ave'  ]