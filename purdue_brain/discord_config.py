import asyncio

import discord
import os
from dotenv import load_dotenv

from purdue_brain.commands.AddNessie import UserAddApiKey
from purdue_brain.commands.HelloWorld import UserCommandHelloWorld
from purdue_brain.commands.NewCommand import UserCommandNewCommand
from purdue_brain.commands.deposit import UserCommandDeposit
from purdue_brain.commands.help import UserCommandHelp
from purdue_brain.commands.TradeHelp import UserCommandTradeHelp
from purdue_brain.commands.Trade import UserCommandTrade
from purdue_brain.commands.price import UserCommandPrice
from purdue_brain.commands.info import UserCommandInfo
from purdue_brain.commands.command import UserCommand
from purdue_brain.commands.tradeInfo import UserCommandTradeInfo
from purdue_brain.common import UserResponse
from purdue_brain.common.utils import iterate_commands, create_simple_message
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
        ('$add_bank', UserAddApiKey),
        ('$hi', UserCommand), ('$helloworld', UserCommandHelloWorld),
        ('$natalie', UserCommandNewCommand), ('$price', UserCommandPrice), ('$info', UserCommandInfo),
        ('$trade_info', UserCommandTradeInfo), ('$help', UserCommandHelp), ('$trade_help', UserCommandTradeHelp),
        ('$order', UserCommandTrade), ('$deposit', UserCommandDeposit)
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


@client.event
async def on_ready():
    pass


async def my_background_task():
    await client.wait_until_ready()
    counter = 0
    discord_channel = int(os.getenv('DISCORD_CHANNEL'))
    channel = client.get_channel(discord_channel)
    while True:
        counter += 1
        message = create_simple_message('Hello There', f'counter: {counter}')
        await channel.send(embed=message)
        await asyncio.sleep(10)  # task runs every 60 seconds


def run_discord():
    client.loop.create_task(my_background_task())
    client.run(os.getenv('TOKEN'))
