import discord
import json
import random
import utilities
import asyncio
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
countdownTimer = int(data['countdownTimer'])

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    

    print("bot online!!!")
    
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

    #if the user gives a string
    try:
        newTimer = int(newTimer)
    except:
        await ctx.reply('Please choose a valid timer. The format should be `!countdown (positive Integer)`')
        return

    #if for whatever reason the message is from the bot
    if ctx.author == bot:
        return
    
    #if the user gives a negative number
    if newTimer < 0:
        await ctx.reply('Please choose a valid timer. The format should be `!countdown (positive Integer)`')
        return
    
    minutes, seconds = divmod(newTimer, 60)

    await ctx.reply('Countdown timer set to ' + str(minutes) + ' minutes and ' + str(seconds) + ' seconds.' )

    with open('botinfo.json') as f:
        temp = json.load(f)
    
    temp['countdownTimer'] = str(newTimer)

    with open('botinfo.json', 'w') as f:
        json.dump(temp, f, ensure_ascii=False, indent=4)

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

    print("entered countdown!\nduration: " + str(countdownTimer) + " seconds")

    time = countdownTimer

    while time:
        time -= 1
        await asyncio.sleep(1)

bot.run(TOKEN)