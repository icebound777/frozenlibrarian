# bot.py
"""Chat bot for the discord chat software"""
import os
import json
import datetime
import asyncio

import discord
from discord.ext import commands
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
    print('File channelnames_to_gametitles.json not found on startup.')

# Eventhandling
@bot.event
async def on_ready():
    """Initial actions after starting up"""
    log_print(f'{bot.user} has connected to Discord!')

    log_print('\nConnected to following servers:')
    for guild in bot.guilds:
        print(f'\"{guild.name}\" (id: {guild.id})')

        #guild.fetch_members()
        #for member in guild.members:
        #    print(f'Member: {member.name}')

    for guild in bot.guilds:
        print(f'  {guild.name}')
        for channel in guild.channels:
            if (channel.type == discord.ChannelType.voice and not channel.category):
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
@bot.command(name='config')
@commands.has_role('admin')
async def cmd_config(ctx, *args):
    log_cmd_details(ctx)
    #hooray = 'args: {}'.format(', '.join(args))
    #print(f'{hooray}')

@bot.command(name='ctog')
async def cmd_test(ctx):
    log_cmd_details(ctx)
    try:
        if dict_channel_to_game is None:
            print('if dict_channel_to_game is None')
    except:
        print('except') # <-
    else:
        await channelnames_to_gametitles()

async def repeat_cmd_test():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await channelnames_to_gametitles()
        await asyncio.sleep(60 * 5)

# Functions
async def channelnames_to_gametitles():
    # For all the guilds the bot is member of
    for bot_guild in bot.guilds:
        # For all the guilds set up in the config-file
        for config_guild in dict_channel_to_game.get('guilds'):
            guild_id = int(config_guild.get('id'))
            if bot_guild.id == guild_id:
                # For all this guild's channels set up in the config-file
                for config_channels in config_guild.get('allowed_channels'):
                    channel_id = int(config_channels.get('id'))
                    channel_name_default = config_channels.get('defaultname')
                    voice_channel = bot_guild.get_channel(channel_id)
                    # If channel does not exist
                    if voice_channel is None:
                        log_print(f'Channel "{bot_guild.name}".{channel_id} '
                                  f'(Default: "{channel_name_default}") does not exist')
                    # Channel is empty and name is not default
                    elif (len(voice_channel.members) == 0
                        and voice_channel.name != channel_name_default):
                        log_print(f'Changed channel "{voice_channel.name}" to '
                                  f'{channel_name_default}')
                        await voice_channel.edit(name=channel_name_default)
                    # Channel is not empty, don't care about channel name
                    elif len(voice_channel.members) > 0:
                        dict_membergames = {}
                        #print(f'{voice_channel.name}')
                        for channel_member in voice_channel.members:
                            if (channel_member.activity is not None
                                and channel_member.activity.type == discord.ActivityType.playing):
                                member_game = channel_member.activity.name
                                dict_membergames[member_game] = dict_membergames.get(member_game, 0) + 1
                                #print(f'  {channel_member.display_name}: '
                                #      f'{member_game}')
                            else:
                                dict_membergames['None'] = dict_membergames.get('None', 0) + 1
                        # Sort played games by amount of players per game, decreasing
                        sorted_membergames = {}
                        sorted_keys = sorted(dict_membergames,
                                             key=dict_membergames.get,
                                             reverse=True)
                        for w in sorted_keys:
                            sorted_membergames[w] = dict_membergames[w]
                        #print(sorted_membergames)
                        for most_played_key in sorted_membergames:
                            if most_played_key != 'None':
                                if (most_played_key != voice_channel.name
                                    and (sorted_membergames.get(voice_channel.name, 0)
                                         < sorted_membergames.get(most_played_key))):
                                    log_print(f'Changed channel "{voice_channel.name}" to '
                                              f'{most_played_key}')
                                    await voice_channel.edit(name=most_played_key)
                                break
                            elif (len(sorted_membergames) == 1
                                and voice_channel.name != channel_name_default):
                                # Members in channel, but nobody is playing: Reset channel name
                                log_print(f'Changed channel "{voice_channel.name}" to '
                                          f'{channel_name_default}')
                                await voice_channel.edit(name=channel_name_default)
                                break

# Helper-Functions
def log_cmd_details(ctx):
    cmd_details = 'Cmd: "' + ctx.message.content + '" (by ' + ctx.author + ' in ' \
                  + ctx.guild.name + '.' + ctx.channel.name + ')'
    log_print(cmd_details)

def log_print(printtext):
    now = datetime.datetime.now()
    logdate = now.strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{logdate}] {printtext}')

# Start bot
bot.loop.create_task(repeat_cmd_test())

bot.run(TOKEN)
