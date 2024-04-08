import discord
import json
import random
import utilities
import asyncio
import tracemalloc
import re

from discord.ext import commands
from discord import FFmpegPCMAudio

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents = intents)

with open ('botinfo.json', 'r') as read_file:
    data = json.load(read_file)

TOKEN = data['token']
serverid = int(data['goonserverid'])
testingserverid = int(data['testingserverid'])
songs = utilities.setupDurations(data)
populatedChannels = []
countdownTimer = 60.0

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    
    print("bot online!$$")
    
    #need to create a command that enables and disables the bot's function to join voice channels.

    while True:
        await playSong()
        await countdown()

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    
    await bot.process_commands(message)   

@bot.command()
async def countdown(ctx, newTimer):

    #add try except for when users dont give correct arguements!

    newTimer = int(newTimer)

    if ctx.author == bot:
        return
    
    if newTimer < 0:
        await ctx.reply("To countdown πρεπει να ειναι θετικος αριθμος ΖΩΟΟΟΟΟ")
        return
    
    print(newTimer)

async def playSong():

    #search for all the channels that have members in them
    populatedChannels = utilities.checkChannels(bot, testingserverid)

    #if no channels with members exist start the countdown, and check again after the countdown ends.
    if len(populatedChannels) == 0:
        return

    #get the most populated out of all the channels
    channel = utilities.mostPopulated(populatedChannels)

    #pick a random song and setup a random duration.
    randomSong = random.choice(songs)

    client = await channel.connect()

    source = FFmpegPCMAudio(randomSong)
    player = client.play(source)

    while client.is_playing():
        await asyncio.sleep(1)
    else:
        await client.disconnect()

async def countdown():

    print("entered countdown!")

    time = countdownTimer

    while time:
        time -= 1
        await asyncio.sleep(1)

bot.run(TOKEN)