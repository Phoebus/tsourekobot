import discord
import json
import random
import utilities
import asyncio
import requests

from discord.ext import commands
from discord import FFmpegPCMAudio

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents = intents)

with open ('botinfo.json', 'r') as read_file:
    data = json.load(read_file)

TOKEN: str = data['token']
serverid: int = int(data['goonserverid'])
testingserverid: int = int(data['testingserverid'])
countdownTimer: int = int(data['countdownTimer'])
SteamKey: str = data['steamkey']

songs: list = utilities.setupDurations(data)
populatedChannels: list = []
active: bool = False

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():

    print("bot online!!!")

    response = requests.get('http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=730&count=6&maxlength=300&format=json')
    responseText = json.loads(response.text)
    #print(responseText['appnews']['newsitems'][0]['url'])

    for news in responseText['appnews']['newsitems']:
        print(news['url'])

    while True:
        await playSong()
        await countdown()

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    
    await bot.process_commands(message)   

@bot.command(help = "This command will either enable or disable the bot's behaviour. On activation the bot will join a voice channel every time the countdown ends. For info on how to change the countdown timer use !help countdown")
async def activate(ctx):

    global active
    active = not active

    if active:
        await ctx.reply('The bot will now join channels automatically')
    else:
        await ctx.reply('The bot has been deactivated')

    return

@bot.command(help = "Specify every how many seconds the bot will scan the voice channels and join the one with the most members. The number should be a positive integer")
async def countdown(ctx, newTimer):

    global countdownTimer

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

    countdownTimer = newTimer

    with open('botinfo.json') as f:
        temp = json.load(f)
    
    temp['countdownTimer'] = str(newTimer)

    with open('botinfo.json', 'w') as f:
        json.dump(temp, f, ensure_ascii=False, indent=4)

async def playSong():

    global active

    if not active:
        print("cycle skipped")
        return

    #search for all the channels that have members in them
    populatedChannels = utilities.checkChannels(bot, serverid)

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