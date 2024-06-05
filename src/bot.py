import os
from discord import Intents, Client, Message
from discord.ext import commands
from dotenv import load_dotenv
import responses
import joblib
import psycopg2

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BS_API_KEY = os.getenv('BS_API_KEY')
intents = Intents.default()
intents.message_content = True
#client = Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

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
@bot.event
async def on_ready() -> None:
    print(f"{bot.user} is now running!")
    await bot.tree.sync()


@bot.hybrid_command(description="Compares two players using a specified brawler to predict the winner of a 1v1 match.")
async def predict1v1(ctx, brawler: str, player1: str, player2: str):
    if ctx.author == bot.user:  # Prevent bot from responding to itself
        return
    
    #print(f"BRAWLLLERR: {brawler}")
    
    def get_player_tag(player):
        # Check if input is a Discord mention
        if player.startswith('<@') and player.endswith('>'):
            player_id = player.strip('<@!>')  # Clean up the mention to get the ID
            cur.execute("SELECT player_tag FROM brawl_stars WHERE discord_id = %s", (player_id,))
            result = cur.fetchone()
            if result:
                return result[0]  # Return the Brawl Stars tag linked to the Discord account
            return None  # If not registered, return None to handle it appropriately
        return player  # If it's not a mention, assume it's a direct player tag

    conn = psycopg2.connect("dbname=test user=postgres")
    cur = conn.cursor()

    player1_tag = get_player_tag(player1)
    player2_tag = get_player_tag(player2)

    if not player1_tag or not player2_tag:
        await ctx.send("Could not retrieve tags for one or both players. Please ensure tags are correctly formatted or registered.")
        cur.close()
        conn.close()
        return

    player1_stats = responses.get_player_metrics(player1_tag, brawler)
    player2_stats = responses.get_player_metrics(player2_tag, brawler)
    
    cur.close()
    conn.close()

    # Ensure both players' stats could be fetched
    if not player1_stats or not player2_stats:
        await ctx.send("Error fetching player statistics. Please check the tags and brawler names.")
        return

    prediction_embed = responses.predict_outcome(player1_stats, player2_stats, player1_stats['player_name'], player2_stats['player_name'])
    await ctx.send(embed=prediction_embed)



@bot.hybrid_command(description="Register your Brawl Stars account!") 
async def register(ctx, player_tag: str):
    if ctx.author == bot.user:
        return
    
    if not responses.get_player(player_tag):
        await ctx.send("Player tag not valid. Please enter a valid Brawl Stars player tag.")
    
    conn = psycopg2.connect("dbname=test user=joshuamatni")
    cur = conn.cursor()
    
    # Check if the user is already registered
    cur.execute("SELECT player_tag FROM brawl_stars WHERE discord_id = %s", (ctx.author.id,))
    result = cur.fetchone()
    
    if result:
        # If already registered, notify the user with their registered tag
        await ctx.send(f"You are already registered with tag {result[0]}!")
    else:
        # If not registered, insert new user data into the database
        cur.execute("INSERT INTO brawl_stars (discord_id, player_tag) VALUES (%s, %s)",
                    (ctx.author.id, player_tag))
        conn.commit()  # Commit the transaction to save changes to the database
        await ctx.send(f"Your Brawl Stars tag '{player_tag}' has been registered successfully!")

    cur.close()
    conn.close()

def main() -> None:
    #bot.add_cog(PrometheusCog(bot))
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()