import os
import pandas as pd
from itertools import combinations
from sklearn.preprocessing import MinMaxScaler

directory = 'clubs/'  # Directory containing all CSV files
all_matchups = []  # List to store data from all files

weights = {
    'brawler_rank': 3,  # Higher weight because rank is most important
    '3vs3_victories': 2,
    'highest_account_trophies': 1,
    'exp_level': 0.5  # Lower weight because exp level is less important
}

scaler = MinMaxScaler()

def calculate_weighted_score(row):
    score = 0
    for feature, weight in weights.items():
        score += row[feature] * weight
    return score

def determine_winner(row, df):
    player1 = df.loc[row['Player1']]
    player2 = df.loc[row['Player2']]
    return player1['player_name'] if player1['score'] > player2['score'] else player2['player_name']

for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)

        # Scale the selected columns
        columns_to_scale = ['brawler_rank', '3vs3_victories', 'highest_account_trophies', 'exp_level']
        df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

        # Calculate score for each row in the DataFrame using weights
        df['score'] = df.apply(calculate_weighted_score, axis=1)

        # Generate all matchups
        matchups = pd.DataFrame(list(combinations(df.index, 2)), columns=['Player1', 'Player2'])
        
        # Apply the function to determine the winner of each matchup
        matchups['Winner'] = matchups.apply(lambda row: determine_winner(row, df), axis=1)

        # Merge additional information about the players in each matchup
        matchups = matchups.merge(df[['player_name', 'score']], left_on='Player1', right_index=True)
        matchups = matchups.rename(columns={'player_name': 'Player1_Name', 'score': 'Player1_Score'})
        matchups = matchups.merge(df[['player_name', 'score']], left_on='Player2', right_index=True)
        matchups = matchups.rename(columns={'player_name': 'Player2_Name', 'score': 'Player2_Score'})

        all_matchups.append(matchups)

# Concatenate all dataframes into one
final_dataset = pd.concat(all_matchups, ignore_index=True)
final_dataset.to_csv('final_matchup_outcomes.csv', index=False)
print("All matchup outcomes saved to final_matchup_outcomes.csv")



