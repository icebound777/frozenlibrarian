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

# Start bot
bot.run(TOKEN)
