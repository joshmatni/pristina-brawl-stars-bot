from random import choice, randint
import requests, os
from dotenv import load_dotenv
import joblib
import pandas as pd
import numpy as np
from sklearn.discriminant_analysis import StandardScaler
from sklearn.preprocessing import MinMaxScaler


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
    load_dotenv()
    BS_API_KEY = os.getenv('BS_API_KEY')
    url = f'https://api.brawlstars.com/v1/players/%23{player_tag.replace("#", "")}'
    headers = {'Authorization': f'Bearer {BS_API_KEY}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_player_metrics(player_tag: str, specific_brawler: str):
    if player_tag.startswith('#'):
        player_tag = player_tag[1:]
    player_info = get_player(player_tag)
    if player_info:
        brawlers_info = player_info.get('brawlers', [])
        # Filter to include only the specific brawler
        brawler_info = next((brawler for brawler in brawlers_info if brawler['name'].upper() == specific_brawler.upper()), None)
        if brawler_info:
            return {
                'player_tag': player_tag,
                'player_name': player_info.get('name', 'Unknown'),
                'brawler_name': brawler_info['name'],
                'rank': brawler_info['rank'],
                'highest_trophies': brawler_info['highestTrophies'],
                '3vs3_victories': player_info.get('3vs3Victories', 0),
                'exp_level': player_info.get('expLevel', 0)
            }
    return None


def get_brawler_list() -> list:
    brawler_list = [
            "Shelly", "Colt", "Brock", "Bull", "Jessie", "Nita", "Dynamike", 
            "El Primo", "Barley", "Poco", "Rosa", "Rico", "Darryl", "Penny", 
            "Carl", "Piper", "Pam", "Frank", "Bibi", "Bea", "Nani", "Edgar", 
            "Griff", "Grom", "Buzz", "Ash", "Bonnie", "Squeak", "Surge", "Colette", 
            "Colonel Ruffs", "Belle", "Lou", "Gus", "Janet", "Otis", "Sam", "Meg", 
            "Mandy", "R-T", "Byron", "Sprout", "Amber", "Gale", "Leon", "Sandy", 
            "Emz", "Mortis", "Tara", "Gene", "Max", "Mr. P", "Spike", "Crow", 
            "Leon", "Sandy", "Gale", "Surge", "Colette", "Lou", "Colonel Ruffs", 
            "Belle", "Byron", "Squeak", "Griff", "Ash", "Meg", "Lola", "Fang"
        ]
    return brawler_list

def calculate_weighted_score(player_stats):
    weights = {'rank': 3, '3vs3_victories': 2, 'highest_trophies': 1, 'exp_level': 0.5}
    score = sum(player_stats[key] * weight for key, weight in weights.items())
    return score

def predict_outcome(player1_stats, player2_stats, player1_name, player2_name):
    player1_score = calculate_weighted_score(player1_stats)
    player2_score = calculate_weighted_score(player2_stats)

    data = {
        'Player1_Score': [player1_score],
        'Player2_Score': [player2_score]
    }
    df = pd.DataFrame(data)

    # Apply the pre-fitted scaler's transform method
    df_scaled = scaler.transform(df)  # Use transform, NOT fit_transform
    
    # Make prediction
    outcome = model.predict(df_scaled)
    winner_name = player1_name if outcome[0] else player2_name

    message = f"{player1_name} scored {player1_score:.2f} and {player2_name} scored {player2_score:.2f}. Winner: {winner_name}."
    return message

