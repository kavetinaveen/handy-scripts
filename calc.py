import pandas as pd

df = pd.read_csv('./tuekysuperlig.csv', engine='python')
df['Date'] = pd.to_datetime(df['Date'], format="%d.%m.%Y")
df = df.sort_values(['Date']).reset_index(drop=True)
df['HomeTeam'] = df['HomeTeam'].apply(lambda x: ''.join(e for e in x if e.isalnum()))
df['AwayTeam'] = df['AwayTeam'].apply(lambda x: ''.join(e for e in x if e.isalnum()))

df_1_2 = df.copy()
df_1_2['Number_Home'] = None
df_1_2['Win_Home'] = None
df_1_2['WinPercentage_Home'] = None
df_1_2['WinPercentage_Home_3'] = None
df_1_2['Number_Away'] = None
df_1_2['Win_Away'] = None
df_1_2['WinPercentage_Away'] = None
df_1_2['WinPercentage_Away_3'] = None
for i in range(len(df_1_2)):
    date = df_1_2.loc[i, 'Date']
    hteam = df_1_2.loc[i, 'HomeTeam']
    ateam = df_1_2.loc[i, 'AwayTeam']
    df_sub = df_1_2[df_1_2['Date'] < date].reset_index(drop=True)
    if len(df_sub) > 0:
        df_sub_home = df_sub[(df_sub['HomeTeam']==hteam) | (df_sub['AwayTeam']==hteam)].reset_index(drop=True)
        df_sub_away = df_sub[(df_sub['AwayTeam']==ateam) | (df_sub['HomeTeam']==ateam)].reset_index(drop=True)
        if len(df_sub_home) > 0:
            df_sub_home['WinningTeam'] = df_sub_home.apply(lambda x: x['HomeTeam'] if x['HomePts'] > x['AwayPts'] else x['AwayTeam'], axis=1)
            df_sub_home['WinningTeam'] = df_sub_home.apply(lambda x: 'Tie' if x['HomePts'] == x['AwayPts'] else x['WinningTeam'], axis=1)
            df_sub_home_3 = df_sub_home.tail(3)
            df_1_2.loc[i, 'Number_Home'] = len(df_sub_home)
            df_1_2.loc[i, 'Win_Home'] = len(df_sub_home[df_sub_home['WinningTeam']==hteam])
            df_1_2.loc[i, 'WinPercentage_Home'] = len(df_sub_home[df_sub_home['WinningTeam']==hteam])/len(df_sub_home)
            df_1_2.loc[i, 'WinPercentage_Home_3'] = len(df_sub_home_3[df_sub_home_3['WinningTeam']==hteam])/len(df_sub_home_3)
        if len(df_sub_away) > 0:
            df_sub_away['WinningTeam'] = df_sub_away.apply(lambda x: x['HomeTeam'] if x['HomePts'] > x['AwayPts'] else x['AwayTeam'], axis=1)
            df_sub_away['WinningTeam'] = df_sub_away.apply(lambda x: 'Tie' if x['HomePts'] == x['AwayPts'] else x['WinningTeam'], axis=1)
            df_sub_away_3 = df_sub_away.tail(3)
            df_1_2.loc[i, 'Number_Away'] = len(df_sub_away)
            df_1_2.loc[i, 'Win_Away'] = len(df_sub_away[df_sub_away['WinningTeam']==ateam])
            df_1_2.loc[i, 'WinPercentage_Away'] = len(df_sub_away[df_sub_away['WinningTeam']==ateam])/len(df_sub_away)
            df_1_2.loc[i, 'WinPercentage_Away_3'] = len(df_sub_away_3[df_sub_away_3['WinningTeam']==ateam])/len(df_sub_away_3)

df_3 = df.copy()
hTeam = df_3['HomeTeam'].unique()
df_3['Number_Hometeam'] = None
df_3['Score_Hometeam'] = None
df_3['WinPercentage_Hometeam_step_3'] = None
for h in hTeam:
    df_3.loc[df_3['HomeTeam']==h, 'Number_Hometeam'] = range(len(df_3[df_3['HomeTeam']==h]))
    df_3.loc[df_3['HomeTeam']==h, 'Score_Hometeam'] = df_3[df_3['HomeTeam']==h].apply(lambda x: 1 if x['HomePts'] > x['AwayPts'] else 0, axis=1)
    df_3.loc[df_3['HomeTeam']==h, 'Score_Hometeam'] = df_3.loc[df_3['HomeTeam']==h, 'Score_Hometeam'].cumsum()
    df_3.loc[df_3['HomeTeam']==h, 'Score_Hometeam'] = df_3.loc[df_3['HomeTeam']==h, 'Score_Hometeam'].shift()
df_3['Score_Hometeam'] = df_3['Score_Hometeam'].fillna(0)
df_3['WinPercentage_Hometeam_step_3'] = df_3['Score_Hometeam']/df_3['Number_Hometeam'].apply(lambda x: max(x, 1))
df_3.loc[df_3['Number_Hometeam'] == 0, 'WinPercentage_Hometeam_step_3'] = None

aTeam = df_3['AwayTeam'].unique()
df_3['Number_Awayteam'] = None
df_3['Score_Awayteam'] = None
df_3['WinPercentage_Awayteam_step_3'] = None
for a in aTeam:
    df_3.loc[df['AwayTeam']==a, 'Number_Awayteam'] = range(len(df_3[df_3['AwayTeam']==a]))
    df_3.loc[df['AwayTeam']==a, 'Score_Awayteam'] = df_3[df_3['AwayTeam']==a].apply(lambda x: 1 if x['AwayPts'] > x['HomePts'] else 0, axis=1)
    df_3.loc[df['AwayTeam']==a, 'Score_Awayteam'] = df_3.loc[df_3['AwayTeam']==a, 'Score_Awayteam'].cumsum()
    df_3.loc[df['AwayTeam']==a, 'Score_Awayteam'] = df_3.loc[df_3['AwayTeam']==a, 'Score_Awayteam'].shift()
df_3['Score_Awayteam'] = df_3['Score_Awayteam'].fillna(0)
df_3['WinPercentage_Awayteam_step_3'] = df_3['Score_Awayteam']/df_3['Number_Awayteam'].apply(lambda x: max(x, 1))
df_3.loc[df_3['Number_Awayteam'] == 0, 'WinPercentage_Awayteam_step_3'] = None

df_3 = df_3.drop(['Number_Hometeam', 'Score_Hometeam', 'Number_Awayteam', 'Score_Awayteam'], axis=1)
df_3 = df_3.where(pd.notnull(df_3), None)

df_final = df_1_2.merge(df_3[['Date', 'HomeTeam', 'AwayTeam', 'WinPercentage_Hometeam_step_3', 'WinPercentage_Awayteam_step_3']], on=['Date', 'HomeTeam', 'AwayTeam'], how='left')

df_final.to_csv('output.csv', index=False)
