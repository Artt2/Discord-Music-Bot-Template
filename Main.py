import os
import discord
from discord.ext import commands
import youtube_dl
from dotenv import load_dotenv  #use dotenv to load TOKEN from .env-file

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all() #intents allow bot developers to 'subscribe' to specific events in Discord
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents = intents)
bot.remove_command('help')  #define function 'help' later

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
    if ctx.author.voice is not None:
        #await ctx.send("Author is currently in the voice channel.")

        voice_channel = ctx.author.voice.channel   #authors voice channel

        if ctx.voice_client is None:    #if bot not in a voice channel, move to authors voice_channel
            vc = await voice_channel.connect()
        else:   #if bot already in a voice channel, move to authors voice_channel
            await ctx.voice_client.move_to(voice_channel)
            vc = ctx.voice_client
            
        """player = await voice_channel.create_ytdl_player(url)
        player.start()"""

        ydl_opts = {'format': 'bestaudio', 'noplaylist': True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url = info['formats'][0]['url']
            ctx.voice_client.play(discord.FFmpegPCMAudio(url), after=lambda e: print(f'Player error: {e}') if e else None)

        
    else:
        await ctx.send("You need to be in a voice channel to use this command!")
        

@play.error
async def play_error(ctx, error):
     """Handling errors in for the play command: invalid arguments"""
     if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        return await ctx.send("Try again with a valid url.")

@bot.command(name = "exit", description = "Make the bot leave the authors voice channel.")
async def exit(ctx):
    voice_state = ctx.guild.me.voice    #bots voice_state
    if voice_state is None:     # if bot not connected to a voice channel
        return await ctx.send("Can't leave a voice channel as I am not connected to one.")
    
    author_voice_state = ctx.author.voice
    if author_voice_state is None:      # if author not in voice channel
        return await ctx.send("You need to be in a voice channel to use this command!")

    if voice_state.channel != author_voice_state.channel:       #if author not in same channel as bot
        return await ctx.send("You need to be in the same voice_channel.")

    # Disconnect from the voice channel
    await ctx.guild.voice_client.disconnect()


bot.run(TOKEN)