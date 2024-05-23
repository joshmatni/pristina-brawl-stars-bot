import os
from discord import Intents, Client, Message
from dotenv import load_dotenv
import responses

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BS_API_KEY = os.getenv('BS_API_KEY')
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("Message was empty... (Intents not enabled properly")
        return
    
    if is_private := user_message[0] == "?":
        user_message = user_message[1:]
    
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e) # replace with logging


# handle start up for bot
@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running!")

@client.event # handles incoming messages
async def on_message(message: Message) -> None:
    if message.author == client.user:  # so bot doesn't infinitely respond to itself
        return

    content = message.content
    if content.startswith('!bsrank '):
        args = content.split(' ')[1:]  # Split the command into parts after '!bsrank'
        if len(args) < 2:
            await message.channel.send("Please provide both a player tag and a brawler's name.")
            return

        player_tag, brawler_name = args[0], ' '.join(args[1:])
        if player_tag[0] == '#':
            player_tag = player_tag[1:]
        player_tag = player_tag.upper()

        try:
            player_stats = responses.get_player_stats(player_tag)
            trophies = player_stats.get('trophies', 'N/A')
            expLevel = player_stats.get('expLevel', 'N/A')
            vs3Victories = player_stats.get('3vs3Victories', 'N/A')

            # Find the specified brawler in the list
            brawlers_info = player_stats.get('brawlers', [])
            brawler_info = next((brawler for brawler in brawlers_info if brawler['name'].upper() == brawler_name.upper()), None)

            if brawler_info:
                brawler_stats = (f"Brawler Name: {brawler_info['name']}, Rank: {brawler_info['rank']}, "
                                f"Trophies: {brawler_info['trophies']}, Highest Trophies: {brawler_info['highestTrophies']}")
                message_to_send = f"Brawler Stats: {brawler_stats}"
            else:
                message_to_send = "No such brawler found."

            await message.channel.send(f"Player and Brawler Info: {message_to_send}")
        except Exception as e:
            await message.channel.send(f"Error fetching player info: {str(e)}")


    elif content.startswith('!predict1v1 '):
        args = content.split(' ')[1:]  # Get arguments after command
        if len(args) != 3:
            await message.channel.send("Usage: !predict1v1 <brawler> <player1> <player2>")
            return

        brawler, player1_tag, player2_tag = args
        try:
            # Fetch player stats
            player1_stats = responses.get_player_stats(player1_tag)
            player2_stats = responses.get_player_stats(player2_tag)
            # Predict outcome
            prediction = responses.predict_outcome(player1_stats, player2_stats, brawler)
            await message.channel.send(f"Prediction: {prediction}")
        except Exception as e:
            await message.channel.send(f"Error processing prediction: {str(e)}")

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
