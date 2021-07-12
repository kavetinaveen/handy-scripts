import pandas as pd

df = pd.read_csv('./tuekysuperlig.csv', engine='python')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(['Date']).reset_index(drop=True)

df['HomeTeam'] = df['HomeTeam'].apply(lambda x: ''.join(e for e in x if e.isalnum()))
df['AwayTeam'] = df['AwayTeam'].apply(lambda x: ''.join(e for e in x if e.isalnum()))

df['WinningTeam'] = df.apply(lambda x: x['HomeTeam'] if x['HomePts'] > x['AwayPts'] else x['AwayTeam'], axis=1)
df['WinningTeam'] = df.apply(lambda x: 'Tie' if x['HomePts'] == x['AwayPts'] else x['WinningTeam'], axis=1)

tmp1 = df[['Date', 'HomeTeam', 'WinningTeam']]
tmp1.columns = ['Date', 'Team', 'WinningTeam']
tmp2 = df[['Date', 'AwayTeam', 'WinningTeam']]
tmp2.columns = ['Date', 'Team', 'WinningTeam']
df_expand = pd.concat([tmp1, tmp2])
df_expand.sort_values(['Date'], inplace=True)

team = df_expand['Team'].unique()
df_expand['Number'] = None
df_expand['Score'] = None
df_expand['WinPercentage'] = None
for t in team:
    df_expand.loc[df_expand['Team']==t, 'Number'] = range(len(df_expand[df_expand['Team']==t]))
    df_expand.loc[df_expand['Team']==t, 'Score'] = df_expand[df_expand['Team']==t].apply(lambda x: 1 if x['WinningTeam'] == t else 0, axis=1)
    df_expand.loc[df_expand['Team']==t, 'Score'] = df_expand[df_expand['Team']==t]['Score'].cumsum()
    df_expand.loc[df_expand['Team']==t, 'Score'] = df_expand[df_expand['Team']==t]['Score'].shift()
df_expand['Score'] = df_expand['Score'].fillna(0)
df_expand['WinPercentage'] = df_expand['Score']/df_expand['Number'].apply(lambda x: max(x, 1))

df_expand.to_csv('output.csv', index=False)
