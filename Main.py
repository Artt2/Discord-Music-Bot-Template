import os
import discord
from dotenv import load_dotenv  # Use dotenv to load TOKEN from .env-file

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all() # Intents allow bot developers to 'subscribe' to specific events in Discord
intents.message_content = True

client = discord.Client(command_prefix = "!", intents=intents) 

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    await msg.channel.send('Hello!')

"""@client.command()
async def ping(ctx):
    await ctx.send("Pong!")"""

client.run(TOKEN)