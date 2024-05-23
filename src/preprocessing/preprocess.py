import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()
BS_API_KEY = os.getenv('BS_API_KEY')

def get_player(player_tag: str):
    """Fetch player data from the Brawl Stars API using the player tag."""
    url = f'https://api.brawlstars.com/v1/players/%23{player_tag.replace("#", "")}'
    headers = {'Authorization': f'Bearer {BS_API_KEY}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_player_metrics(player_tags_file: str, specific_brawler='Piper'):
    """Retrieve metrics for multiple players for a specific brawler and store in a DataFrame."""
    player_data = []
    with open(player_tags_file, 'r') as file:
        for line in file:
            player_tag = line.strip()
            if player_tag.startswith('#'):
                player_tag = player_tag[1:]  # Remove the # from the player tag if present
            player_info = get_player(player_tag)
            if player_info:
                brawlers_info = player_info.get('brawlers', [])
                # Filter to include only the specific brawler
                brawler_info = next((brawler for brawler in brawlers_info if brawler['name'].upper() == specific_brawler.upper()), None)
                if brawler_info:
                    data = {
                        'player_tag': player_tag,
                        'brawler_name': brawler_info['name'],
                        'rank': brawler_info['rank'],
                        'trophies': brawler_info['trophies'],
                        'highest_trophies': brawler_info['highestTrophies']
                    }
                    player_data.append(data)
    return pd.DataFrame(player_data)

# Specify the path to your file containing player tags
file_path = 'pristine_ninjas.txt'
df_players = get_player_metrics(file_path, specific_brawler='Piper')

# Write to Excel
excel_path = 'pristineNinjas_piper_metrics.xlsx' 
df_players.to_excel(excel_path, index=False)  # Set index=False to not write row indices
print(f"Data written to {excel_path}")


