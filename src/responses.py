from random import choice, randint
import requests, os
from dotenv import load_dotenv
import joblib
import pandas as pd
import numpy as np
from sklearn.discriminant_analysis import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import discord
load_dotenv()
BS_API_KEY = os.getenv('BS_API_KEY')


# Load the trained model
model = joblib.load('preprocessing/models/bs_1v1_predictor.pkl')
scaler = joblib.load('preprocessing/models/scaler.pkl')

def get_response(user_input: str) -> str: 
    #! insert response/output of AI bot stuff like who wins
    lowered = user_input.lower() 
    if lowered == '':
        return "Well you\'re awfully silent..."
    elif "hello" in lowered:
        return "Hello there!"
    else:
        return choice(["WEE WOO?",
                       "edgar mains...",
                       "BRAWL STARS FOREVAAA!!"])
    raise NotImplementedError("Code is missing...")

def get_player(player_tag: str):
    url = f'https://api.brawlstars.com/v1/players/%23{player_tag.replace("#", "")}'
    headers = {'Authorization': f'Bearer {BS_API_KEY}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("get player")
        return response.json()
    else:
        print("no player")
        return None

def get_player_metrics(player_tag: str, specific_brawler: str):
    player_info = get_player(player_tag)  # Fetch player info
    if player_info:
        for brawler in player_info.get('brawlers', []):
            if brawler['name'].upper() == specific_brawler.upper():
                return {
                    'player_name': player_info.get('name', 'Unknown'),
                    'exp_level': player_info['expLevel'],
                    'highest_account_trophies': player_info['highestTrophies'],
                    '3vs3_victories': player_info['3vs3Victories'],
                    'brawler_name': brawler['name'],
                    'brawler_rank': brawler['rank'],
                    'brawler_id': brawler['id']
                }
    return None  # Return None if no brawler matches

def get_brawler_list():
    url = 'https://api.brawlapi.com/v1/brawlers'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Return the list of brawlers in JSON format
    else:
        return None  # Return None if there was an error with the request

def calculate_weighted_score(player_stats):
    # Assuming typical maximum values for normalization purposes; adjust as real data informs
    print(player_stats)
    max_values = {
        'brawler_rank': 35,  # Typically ranks range from 1 to 35
        '3vs3_victories': 50000,  # Estimated high range for victories
        'highest_account_trophies': 100000,  # Similar high range for trophies
        'exp_level': 500  # Max level observed or expected
    }

    weights = {
        'brawler_rank': 3, 
        '3vs3_victories': 2, 
        'highest_account_trophies': 1, 
        'exp_level': 0.5
    }

    # Normalize each statistic by its assumed maximum and then apply the weight
    normalized_scores = [(player_stats[key] / max_values[key]) * weights[key] for key in weights]
    score = sum(normalized_scores)
    return score

def predict_outcome(player1_stats, player2_stats, player1_name, player2_name):
    player1_score = calculate_weighted_score(player1_stats)
    player2_score = calculate_weighted_score(player2_stats)

    outcome = model.predict([[player1_score, player2_score]])
    winner_name = player1_name if outcome[0] else player2_name

    embed = discord.Embed(title=f"1v1 {player1_stats['brawler_name'].capitalize()} Prediction Result", 
                          description="Comparison and prediction of player performance.", 
                          color=discord.Colour.dark_purple())
    embed.add_field(name=f"{player1_name}", value=f"Score: {player1_score:.2f}\nLevel: {player1_stats['exp_level']}\nTrophies: {player1_stats['highest_account_trophies']}\n3vs3 Victories: {player1_stats['3vs3_victories']}\nRank: {player1_stats['brawler_rank']}", inline=True)
    embed.add_field(name=f"{player2_name}", value=f"Score: {player2_score:.2f}\nLevel: {player2_stats['exp_level']}\nTrophies: {player2_stats['highest_account_trophies']}\n3vs3 Victories: {player2_stats['3vs3_victories']}\nRank: {player2_stats['brawler_rank']}", inline=True)
    embed.add_field(name="Predicted Winner", value=winner_name, inline=False)

    # Set thumbnail using the common brawler ID
    print(player1_stats['brawler_id'])
    print(player1_stats['brawler_name'])
    brawler_icon_url = f"https://cdn.brawlify.com/brawler/{player1_stats['brawler_name'].capitalize()}.png?v=1"
    embed.set_thumbnail(url=brawler_icon_url)
    #embed.set_image(url=brawler_icon_url)

    return embed

if __name__ == '__main__':
    get_player('pucypryg')