#Discord bot - Github second real commit
#TODO: None as of right now, possibly more riot api calls

import discord
import random
import asyncio
from cassiopeia import riotapi
from json import load as json_load

    #-+-+-+-+- LOAD OPTIONS -+-+-+-+-#
class FileHandler:
    options_json = 'options.json'

    @staticmethod
    def load_and_get_token():
        if FileHandler.options_json is None:
            FileHandler.options_json = 'options.json'
        try:
            json_file = open('options.json')
            FileHandler.options_json = json_load(json_file)
            json_file.close()
            return FileHandler.options_json['token']
        except:
            print('Failed to retrieve token, check if JSON syntax is correct.')

    @staticmethod
    def load_and_get_apikey():
        if FileHandler.options_json is None:
            FileHandler.options_json = 'options.json'
        try:
            json_file = open('options.json')
            FileHandler.options_json = json_load(json_file)
            json_file.close()
            return FileHandler.options_json['api-key']
        except:
            print('Failed to retrieve API key, check if JSON syntax is correct.')
    # -+-+-+-+- LOAD END -+-+-+-+-#

client = discord.Client()
riotapi.set_api_key(FileHandler.load_and_get_apikey())
riotapi.set_region('NA')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    #Keeps the bot from replying to itself using >say
    if message.author == client.user:
        return

    #Lists all commands
    if message.content.startswith('>halp'):
        await client.send_message(message.channel,
            '''
              `>say (message): Makes the bot reply with whatever you put afterwards.`
            \n`>save: save her shes being held captive`
            \n`>name: Replies with your name.`
            \n`>rname: Replies with your name. Reversed!`
            \n`>die: OWNER ONLY, kills the bot's process.`
            \n`>randmoji: Replies with a random emoji from the server the message is sent in.`
            \n`>monty: Replies with a random Monty Python clip.`
            \n`>mastery (summoner name) (champion): Replies with the mastery level and points for the args given.`
            \n`>free: Replies with the free rotation for the week.`
            '''
        )
    #Basic Commands
    if message.content.startswith('>say'):
        arg = message.content.split('>say', 1)
        await client.send_message(message.channel, arg[1])
        await client.delete_message(message)

    if message.content.startswith('>save'):
        await client.send_message(message.channel, 'save me im being held captive')
        await client.delete_message(message)

    if message.content.startswith('>name'):
        await client.send_message(message.channel, message.author.name)
        await client.delete_message(message)

    if message.content.startswith('>rname'):
        name = message.author.name
        await client.send_message(message.channel, name[::-1])
        await client.delete_message(message)

    #Kills the bot's process
    if message.content.startswith('>die'):
        if message.author.id == '140329679159689216':
            await client.send_message(message.channel, 'Bot shutting down...')
            exit('Bot shutting down...')

    if message.content.startswith('>randmoji'):
        emotes = []
        for emote in message.server.emojis:
            emotes.append(emote)
        await client.send_message(message.channel, '{}'.format(emotes[random.randrange(0, len(emotes))]))

    if message.content.startswith('>monty'):
        monties = [
            'https://www.youtube.com/watch?v=zIV4poUZAQo',
            'https://www.youtube.com/watch?v=kQFKtI6gn9Y',
            'https://www.youtube.com/watch?v=kQFKtI6gn9Y',
            'https://www.youtube.com/watch?v=zPGb4STRfKw',
            'https://www.youtube.com/watch?v=_84-A3LT0Lo'
            ]
        await client.send_message(message.channel, '{}'.format(monties[random.randrange(0, len(monties))]))

    #RiotAPI Commands
    if message.content.startswith('>mastery'):
        command_remover = message.content.split('>mastery', 1)
        for i in command_remover:
            args = i.split(' ')
        summonerid = riotapi.get_summoner_by_name(args[1])
        championid = riotapi.get_champion_by_name(args[2])
        try:
            mastery = riotapi.get_champion_mastery(summonerid, championid)
        except AttributeError:
            await client.send_message(message.channel, 'Error. Check champion and summoner name spelling.')
        await client.send_message(message.channel, '{0}: {1} \n{2}: {3} \n{4}: {5} \n{6}: {7}'.format('Summoner', args[1], 'Champion', args[2], 'Level', mastery.level, 'Points', mastery.points))

    if message.content.startswith('>free'):
        statuses = riotapi.get_champion_statuses(free_to_play=True)
        free_rotation = []
        for x in statuses:
            free_rotation.append(x.name)
        await client.send_message(message.channel, '{0}: \n{1}'.format('Free Champions this week', free_rotation))

try:
    client.run(FileHandler.load_and_get_token())
    print('Logging in...')
except discord.errors.LoginFailure:
    exit('Login failed, check token.')
