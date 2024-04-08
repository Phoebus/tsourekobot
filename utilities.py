def checkChannels(bot, serverid) -> list:

    populatedChannels = []

    for i in bot.guilds:
        if i.id == serverid:
            for k in i.voice_channels:
                if len(k.members) != 0:
                    populatedChannels.append(k)
    
    return populatedChannels

def mostPopulated(populatedChannels):

    mostPopulatedChannel = populatedChannels[0]

    for channel in populatedChannels:
        if channel.members > mostPopulatedChannel.members:
            mostPopulatedChannel = channel
    
    return mostPopulatedChannel

def setupDurations(data: dict) -> list:

    songs = []

    for name in data['soundsLength']:
        songs.append(name)
    
    return songs
    
