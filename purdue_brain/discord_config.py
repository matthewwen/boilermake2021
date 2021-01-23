import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import random

from purdue_brain.commands.AddNessie import UserGetApiLink, UserAddApiKey
from purdue_brain.commands.HelloWorld import UserCommandHelloWorld
from purdue_brain.commands.NewCommand import UserCommandNewCommand
from purdue_brain.commands.price import UserCommandPrice
from purdue_brain.commands.info import UserCommandInfo
from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse
from purdue_brain.common.utils import iterate_commands
from purdue_brain.wrappers.discord_wrapper import DiscordWrapper
from purdue_brain.wrappers.firebase_wrapper import FirebaseWrapper

load_dotenv()
client = discord.Client()
DiscordWrapper.client = client
DiscordWrapper.fire = FirebaseWrapper()
discord_wrapper = DiscordWrapper()


@client.event
async def on_ready():
    pass


def create_direct_command(content):
    return iterate_commands(content, [
        ('$help_bank', UserGetApiLink), ('$add_bank_key', UserAddApiKey),
        ('$hi', UserCommand), ('$helloworld', UserCommandHelloWorld),
        ('$natalie', UserCommandNewCommand), ('$price', UserCommandPrice), ('$info', UserCommandInfo)
    ])


async def run(obj, message, response):
    if obj is not None:
        inst: UserCommand = obj(message.author, message.content, response)
        await response.send_loading(message)
        await inst.run()


async def handle_direct_message(message, response: UserResponse):
    if not response.done:
        if type(message.channel) is discord.TextChannel and str(message.channel.id) == os.getenv('DISCORD_CHANNEL'):
            content = message.content.lower()
            await run(create_direct_command(content), message, response)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response: UserResponse = UserResponse()
    await handle_direct_message(message, response)
    if response.done:
        await response.send_message(message)
        return


# @client.event
# async def on_message(message):
#     if 'happy birthday' in message.content.lower():
#         await message.channel.send('Happy Birthday! 🎈🎉')

def run_discord():
    client.run(os.getenv('TOKEN'))
