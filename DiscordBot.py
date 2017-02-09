#Simple bot rendition 1
#TODO: Add emoticon references, actually let the bot shut down with a command

import discord
from json import load as json_load
#import asyncio

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
        except FileNotFoundError or OSError:
            print("File not found.")
#-+-+-+-+- LOAD END -+-+-+-+-#

#-+-+-+-+- FUNCTIONALITY -+-+-+-+-#
client = discord.Client()
spam_channel = client.get_channel('172251363110027264')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(">pls"):
        await client.send_message(message.channel, "Functioning as intended :D")
    if message.content.startswith(">name"):
        await client.send_message(message.channel, message.author.name)
    if message.content.startswith(">vulnerable"):
        await client.send_message(message.channel, "Vulnerable? I'll show you vulnerable.")
    if message.content.startswith(">reversename"):
        name = message.author.name
        await client.send_message(message.channel, name[::-1])
    if message.content.startswith(">die"):
        if message.author.name == "Cata":
            await client.send_message(message.channel, "Bot shutting down...")
            exit("Bot shutting down...")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


try:
    client.run(FileHandler.load_and_get_token())
    print("Logging in...")
except discord.errors.LoginFailure:
    exit("Login failed, check token.")
    # -+-+-+-+- END FUNCTIONALITY -+-+-+-+-#