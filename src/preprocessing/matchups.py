import pandas as pd
from itertools import combinations
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv('pristineNinjas_piper_metrics.csv')
weights = {
    'rank': 3,  # Higher weight because rank is most important
    '3vs3_victories': 2,
    'highest_trophies': 1,
    'exp_level': 0.5  # Lower weight because exp level is less important
}

scaler = MinMaxScaler()

# Scale the selected columns
columns_to_scale = ['rank', '3vs3_victories', 'highest_trophies', 'exp_level']
df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

# Calculate score for each row in the DataFrame using weights
def calculate_weighted_score(row):
    score = 0
    for feature, weight in weights.items():
        score += row[feature] * weight
    return score

df['score'] = df.apply(calculate_weighted_score, axis=1)

# Generate all matchups
matchups = pd.DataFrame(list(combinations(df.index, 2)), columns=['Player1', 'Player2'])

# Function to determine the winner based on scores
def determine_winner(row):
    player1 = df.loc[row['Player1']]
    player2 = df.loc[row['Player2']]
    return player1['player_name'] if player1['score'] > player2['score'] else player2['player_name']

# Apply the function to determine the winner of each matchup
matchups['Winner'] = matchups.apply(determine_winner, axis=1)

# merge additional information about the players in each matchup
matchups = matchups.merge(df[['player_name', 'score']], left_on='Player1', right_index=True)
matchups = matchups.rename(columns={'player_name': 'Player1_Name', 'score': 'Player1_Score'})
matchups = matchups.merge(df[['player_name', 'score']], left_on='Player2', right_index=True)
matchups = matchups.rename(columns={'player_name': 'Player2_Name', 'score': 'Player2_Score'})


matchups.to_csv('matchup_outcomes.csv', index=False)
print("Matchup outcomes saved to 'matchup_outcomes.csv'")


