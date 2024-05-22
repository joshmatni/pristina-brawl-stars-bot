from random import choice, randint
import requests, os
from dotenv import load_dotenv
BS_API_KEY = os.getenv('BS_API_KEY')
load_dotenv()

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

def get_player_stats(player_tag: str): # player_tag: str
    BS_API_KEY = os.getenv('BS_API_KEY')
    load_dotenv()
    url = f'https://api.brawlstars.com/v1/players/%23{player_tag}'
    headers = {'Authorization': f'Bearer {BS_API_KEY}'}
    response = requests.get(url, headers=headers)
    return response.json()

def predict_outcome(player1, player2):
    return
