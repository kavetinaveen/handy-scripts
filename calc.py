import pandas as pd

df = pd.read_csv('./tuekysuperlig.csv', engine='python')
df['Date'] = pd.to_datetime(df['Date'], format="%d.%m.%Y")
df = df.sort_values(['Date']).reset_index(drop=True)
df['HomeTeam'] = df['HomeTeam'].apply(lambda x: ''.join(e for e in x if e.isalnum()))
df['AwayTeam'] = df['AwayTeam'].apply(lambda x: ''.join(e for e in x if e.isalnum()))

df['Number_Home'] = None
df['Win_Home'] = None
df['WinPercentage_Home'] = None
df['WinPercentage_Home_3'] = None
df['Number_Away'] = None
df['Win_Away'] = None
df['WinPercentage_Away'] = None
df['WinPercentage_Away_3'] = None
for i in range(len(df)):
    date = df.loc[i, 'Date']
    hteam = df.loc[i, 'HomeTeam']
    ateam = df.loc[i, 'AwayTeam']
    df_sub = df[df['Date'] < date].reset_index(drop=True)
    if len(df_sub) > 0:
        df_sub_home = df_sub[(df_sub['HomeTeam']==hteam) | (df_sub['AwayTeam']==hteam)].reset_index(drop=True)
        df_sub_away = df_sub[(df_sub['AwayTeam']==ateam) | (df_sub['HomeTeam']==ateam)].reset_index(drop=True)
        if len(df_sub_home) > 0:
            df_sub_home['WinningTeam'] = df_sub_home.apply(lambda x: x['HomeTeam'] if x['HomePts'] > x['AwayPts'] else x['AwayTeam'], axis=1)
            df_sub_home['WinningTeam'] = df_sub_home.apply(lambda x: 'Tie' if x['HomePts'] == x['AwayPts'] else x['WinningTeam'], axis=1)
            df_sub_home_3 = df_sub_home.tail(3)
            df.loc[i, 'Number_Home'] = len(df_sub_home)
            df.loc[i, 'Win_Home'] = len(df_sub_home[df_sub_home['WinningTeam']==hteam])
            df.loc[i, 'WinPercentage_Home'] = len(df_sub_home[df_sub_home['WinningTeam']==hteam])/len(df_sub_home)
            df.loc[i, 'WinPercentage_Home_3'] = len(df_sub_home_3[df_sub_home_3['WinningTeam']==hteam])/len(df_sub_home_3)
        if len(df_sub_away) > 0:
            df_sub_away['WinningTeam'] = df_sub_away.apply(lambda x: x['HomeTeam'] if x['HomePts'] > x['AwayPts'] else x['AwayTeam'], axis=1)
            df_sub_away['WinningTeam'] = df_sub_away.apply(lambda x: 'Tie' if x['HomePts'] == x['AwayPts'] else x['WinningTeam'], axis=1)
            df_sub_away_3 = df_sub_away.tail(3)
            df.loc[i, 'Number_Away'] = len(df_sub_away)
            df.loc[i, 'Win_Away'] = len(df_sub_away[df_sub_away['WinningTeam']==ateam])
            df.loc[i, 'WinPercentage_Away'] = len(df_sub_away[df_sub_away['WinningTeam']==ateam])/len(df_sub_away)
            df.loc[i, 'WinPercentage_Away_3'] = len(df_sub_away_3[df_sub_away_3['WinningTeam']==ateam])/len(df_sub_away_3)

df.to_csv('output.csv', index=False)
