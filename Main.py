import os
import discord
from discord.ext import commands
from dotenv import load_dotenv  # Use dotenv to load TOKEN from .env-file

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all() # Intents allow bot developers to 'subscribe' to specific events in Discord
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents = intents)
bot.remove_command('help')  # Define function 'help' later

@bot.event
async def on_ready():
    print(f"Succesfully logged in as {bot.user}")

@bot.command(name = "ping", description = "Ping command for testing")
async def ping(ctx):    #ctx short for context
    await ctx.send("Pong!")

@bot.command(name = "help", description = "General help command")
async def help(ctx):
    await ctx.send(
        """
This bot allows you to play audio in voice channels via Youtube urls.

Start playing songs with **'!play [url]'**.
Queue song with **'!queue [url]**.
Skip song with **'!skip'**.
Pause with **'!pause'**.
Exit with **'!exit'**.

For all commands, see **'!commands'**.
        """
        )

@bot.command(name = "commands", description = "Prints all commands available in alphabetical order")
async def commands(ctx):
    helptext = "```"
    sortedCommands = sorted(bot.commands, key = lambda x: x.name)
    for command in sortedCommands:
        helptext += f"{command}: {command.description}\n"
    helptext+="```"
    await ctx.send(helptext)


@bot.command(name = "play", description = "Joins voice channel where it's called from and plays given url")
async def play(ctx, url):
    """
    Before playing, checks that:
    - url is valid
    - author is in a voice channel
    - bot isnt already on the channel 
    """
    if not_in_voice_channel:
            return await ctx.send("You need to be in a voice channel to use this command!")
    
    vc = ctx.author.voice.channel   #authors voice channel
    
    if ctx.voice_client is None:
        vc = await vc.connect()
    else:
        await ctx.voice_client.move_to(vc)
        vc = ctx.voice_client
        
@play.error
async def play_error(ctx, error):
     """Handling errors in for the play command: invalid arguments"""
     if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        return await ctx.send("Try again with a valid url.")

def not_in_voice_channel(ctx): #TODO: FIX THIS
     """Checks if author is in a voice channel"""
     ctx.author.voice == None or ctx.author.voice.channel == None

bot.run(TOKEN)