import pandas as pd

df = pd.read_csv('./tuekysuperlig.csv', engine='python')
df['Date'] = pd.to_datetime(df['Date'], format="%d.%m.%Y")
df = df.sort_values(['Date']).reset_index(drop=True)

hTeam = df['HomeTeam'].unique()
df['Number_Hometeam'] = None
df['Score_Hometeam'] = None
df['WinPercentage_Hometeam'] = None
for h in hTeam:
    df.loc[df['HomeTeam']==h, 'Number_Hometeam'] = range(len(df[df['HomeTeam']==h]))
    df.loc[df['HomeTeam']==h, 'Score_Hometeam'] = df[df['HomeTeam']==h].apply(lambda x: 1 if x['HomePts'] > x['AwayPts'] else 0, axis=1)
    df.loc[df['HomeTeam']==h, 'Score_Hometeam'] = df.loc[df['HomeTeam']==h, 'Score_Hometeam'].cumsum()
    df.loc[df['HomeTeam']==h, 'Score_Hometeam'] = df.loc[df['HomeTeam']==h, 'Score_Hometeam'].shift()
df['Score_Hometeam'] = df['Score_Hometeam'].fillna(0)
df['WinPercentage_Hometeam'] = df['Score_Hometeam']/df['Number_Hometeam'].apply(lambda x: max(x, 1))

aTeam = df['AwayTeam'].unique()
df['Number_Awayteam'] = None
df['Score_Awayteam'] = None
df['WinPercentage_Awayteam'] = None
for a in aTeam:
    df.loc[df['AwayTeam']==a, 'Number_Awayteam'] = range(len(df[df['AwayTeam']==a]))
    df.loc[df['AwayTeam']==a, 'Score_Awayteam'] = df[df['AwayTeam']==a].apply(lambda x: 1 if x['AwayPts'] > x['HomePts'] else 0, axis=1)
    df.loc[df['AwayTeam']==a, 'Score_Awayteam'] = df.loc[df['AwayTeam']==a, 'Score_Awayteam'].cumsum()
    df.loc[df['AwayTeam']==a, 'Score_Awayteam'] = df.loc[df['AwayTeam']==a, 'Score_Awayteam'].shift()
df['Score_Awayteam'] = df['Score_Awayteam'].fillna(0)
df['WinPercentage_Awayteam'] = df['Score_Awayteam']/df['Number_Awayteam'].apply(lambda x: max(x, 1))

df.to_csv('output.csv', index=False)
