# bot.py
"""Chat bot for the discord chat software"""
import os
import discord
from discord.ext import commands

from dotenv import load_dotenv

# Setup the bot's discord token (from local .env file)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Instancialise client connection
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Events
@bot.event
async def on_ready():
    """Initial actions after starting up"""
    print(f'{bot.user} has connected to Discord!')

    print(f'\nConnected to following servers:')
    for guild in bot.guilds:
        print(f'\"{guild.name}\" (id: {guild.id})')
        
        guild.fetch_members()
        for member in guild.members:
            print(f'Member: {member.name}')

# Commands
@bot.command(name='test', help='Informativer Text hier')
@commands.has_role('admin')
async def cmd_test(ctx):
    #await ctx.send('hooray!')
    print(f'\nVoicechannel-List:')
    for guild in bot.guilds:
        print(f'  {guild.name}')
        for channel in guild.channels:
            if channel.type == discord.ChannelType.voice and not channel.category:
                print(f'    {channel.name}: {channel.type} - {channel.category}')
                for channelmember in channel.members:
                    if channelmember.activity == discord.ActivityType.playing:
                        print(f'{channelmember.name} is playing {channelmember.activity.name}')

# Start bot
bot.run(TOKEN)
