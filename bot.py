# bot.py
"""Chat bot for the discord chat software"""
import os
import discord
from discord.ext import commands
import json

from dotenv import load_dotenv

# Setup the bot's discord token (from local .env file)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Instancialise client connection
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Load general settings

# Load function-specific settings
## Load channelnames_to_gametitles
try:
    with open('channelnames_to_gametitles.json', 'r') as json_file:
        dict_channel_to_game = json.load(json_file)
except:
    print(f'channelnames_to_gametitles.json not found on startup.')

# Eventhandling
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

    for guild in bot.guilds:
        print(f'  {guild.name}')
        for channel in guild.channels:
            if channel.type == discord.ChannelType.voice and not channel.category:
                print(f'    {channel.name}: {channel.type} - {channel.category} / ID: {channel.id}')
                for channelmember in channel.members:
                    if channelmember.activity == discord.ActivityType.playing:
                        print(f'{channelmember.name} is playing {channelmember.activity.name}')

# Commands
""" @bot.command(name='test', help='Informativer Text hier')
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
 """
@bot.command(name='ctog')
async def cmd_test(ctx):
    print(f'Cmd: ctog')
    await channelnames_to_gametitles()

# Functions
async def channelnames_to_gametitles():
    try:
        if dict_channel_to_game is None:
            print(f'if dict_channel_to_game is None')
    except:
        print(f'except') # <-
    else:
        # for all the guilds set up in the config-file
        for config_guild in dict_channel_to_game.get('guilds'):
            guild_id = int(config_guild.get('id'))
            # for all the guilds the bot is member of
            for bot_guild in bot.guilds:
                if bot_guild.id == guild_id:
                    # for all this guild's channels set up in the config-file
                    for config_channels in config_guild.get('allowed_channels'):
                        channel_id = int(config_channels.get('id'))
                        channel_name_default = config_channels.get('defaultname')
                        voice_channel = bot_guild.get_channel(channel_id)
                        # channel is empty and name is not default
                        if len(voice_channel.members) == 0 and voice_channel.name != channel_name_default:
                            await voice_channel.edit(name=channel_name_default)
                        # channel is not empty
                        if len(voice_channel.members) > 0:
                            for channel_member in voice_channel.members:
                                if channel_member.activity.type == discord.ActivityType.playing:
                                    print(f'{channel_member.display_name}: {channel_member.activity.name}')
                                    await voice_channel.edit(name=channel_member.activity.name)
# Start bot
bot.run(TOKEN)
