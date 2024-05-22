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
    if content.startswith('!stats '):
        player_tag = content.split('!stats ')[1].strip()  # Remove any extra spaces
        try:
            battle_log = responses.get_player_stats(player_tag)
            brawlers_info = battle_log.get('brawlers', [])[:3]  # Get the first three brawlers
            if brawlers_info:
                message_to_send = ""
                for brawler in brawlers_info:
                    message_to_send += (f"Name: {brawler['name']}, Power: {brawler['power']}, Rank: {brawler['rank']}, "
                                        f"Trophies: {brawler['trophies']}, Highest Trophies: {brawler['highestTrophies']}\n")
                await message.channel.send(f"Brawler Info: {message_to_send}")
            else:
                await message.channel.send("No brawler information available")
        except Exception as e:
            await message.channel.send(f"Error fetching brawler info: {str(e)}")
    else:
        await send_message(message, content)

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
