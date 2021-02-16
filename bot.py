# bot.py
"""Chat bot for the discord chat software"""
import os
import discord

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    """Initial actions after starting up"""
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
