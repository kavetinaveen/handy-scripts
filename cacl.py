import pandas as pd

df = pd.read_csv('./tuekysuperlig.csv', engine='python')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(['Date']).reset_index(drop=True)

hTeam = df['HomeTeam'].unique()
df['Number_Hometeam'] = None
df['Score_Hometeam'] = None
df['WinPercentage_Hometeam'] = None
for h in hTeam:
    df.loc[df['HomeTeam']==h, 'Number_Hometeam'] = range(1, len(df[df['HomeTeam']==h])+1)
    df.loc[df['HomeTeam']==h, 'Score_Hometeam'] = df[df['HomeTeam']==h].apply(lambda x: 1 if x['HomePts'] > x['AwayPts'] else 0, axis=1)
    df.loc[df['HomeTeam']==h, 'Score_Hometeam'] = df.loc[df['HomeTeam']==h, 'Score_Hometeam'].cumsum()
df['WinPercentage_Hometeam'] = df['Score_Hometeam']/df['Number_Hometeam']

aTeam = df['AwayTeam'].unique()
df['Number_Awayteam'] = None
df['Score_Awayteam'] = None
df['WinPercentage_Awayteam'] = None
for a in aTeam:
    df.loc[df['AwayTeam']==a, 'Number_Awayteam'] = range(1, len(df[df['AwayTeam']==a])+1)
    df.loc[df['AwayTeam']==a, 'Score_Awayteam'] = df[df['AwayTeam']==a].apply(lambda x: 1 if x['AwayPts'] > x['HomePts'] else 0, axis=1)
    df.loc[df['AwayTeam']==a, 'Score_Awayteam'] = df.loc[df['AwayTeam']==a, 'Score_Awayteam'].cumsum()
df['WinPercentage_Awayteam'] = df['Score_Awayteam']/df['Number_Awayteam']

df.to_csv('output.csv', index=False)
