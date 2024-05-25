import pandas as pd
import requests
import os
from dotenv import load_dotenv
import argparse


load_dotenv()
BS_API_KEY = os.getenv('BS_API_KEY')

def get_player(player_tag: str):
    url = f'https://api.brawlstars.com/v1/players/%23{player_tag.replace("#", "")}'
    headers = {'Authorization': f'Bearer {BS_API_KEY}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_player_metrics(player_tag: str, specific_brawler='Piper'):
    """Fetch and process player metrics including account highest trophies and specific brawler details."""
    player_info = get_player(player_tag)  # Fetch player info inside the function
    player_data = []
    if player_info:
        account_data = {
            'player_tag': player_tag,  # Use player_tag directly
            'player_name': player_info.get('name', 'Unknown'),
            'exp_level': player_info['expLevel'],
            'highest_account_trophies': player_info['highestTrophies'],  # Account-wide highest trophies
            '3vs3_victories': player_info['3vs3Victories']
        }

        brawler_info = next((brawler for brawler in player_info.get('brawlers', [])
                            if brawler['name'].upper() == specific_brawler.upper()), None)
        if brawler_info:
            account_data.update({
                'brawler_name': brawler_info['name'],
                'brawler_rank': brawler_info['rank'],
            })
        player_data.append(account_data)

    return player_data



def get_club(club_tag: str):
    if club_tag.startswith('#'):
        club_tag = club_tag[1:]
    headers = {'Authorization': f'Bearer {BS_API_KEY}'}
    url = f'https://api.brawlstars.com/v1/clubs/%23{club_tag}/members'
    club_members_response = requests.get(url, headers=headers)
    if club_members_response.status_code == 200:
        members_data = club_members_response.json()
        members_list = [{'name': member['name'], 'tag': member['tag']} for member in members_data.get('items', [])]
        return members_list
    else:
        return None

def process_club_members(club_tag: str):
    club_members = get_club(club_tag)
    if not club_members:
        return "Failed to fetch club members or no members found."

    all_player_data = []
    for member in club_members:
        player_metrics = get_player_metrics(member['tag'], 'Piper')
        all_player_data.extend(player_metrics)

    return pd.DataFrame(all_player_data)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('club_tags', type=str, nargs='+', help='A list of club tags to process')
    return parser.parse_args()

def main():
    file_path = 'club_tags.txt'
    with open(file_path, 'r') as file:
        for line in file:
            club_tag = line.strip()  # Remove any leading/trailing whitespace
            if club_tag.startswith('#'):
                club_tag = club_tag[1:]  # Remove the hash if hash

            result = process_club_members(club_tag)
            if isinstance(result, pd.DataFrame):
                filename = f'clubs/{club_tag}_members.csv'
                result.to_csv(filename, index=False)
                print(f"Data saved to {filename}")
            else:
                print(result)

if __name__ == "__main__":
    main()




