import os
import asyncio as asyncio
import discord
from discord import Game, Embed

from utility import ConfigManager
import STATICS
import onlinetime_manager
import role_manager
from commands import cmd_ping, cmd_autorole, cmd_sortConfig

client = discord.Client()
cm = ConfigManager
join_time = {}

commands = {

    "autorole": cmd_autorole,
    "ping": cmd_ping,
    "sortConfig": cmd_sortConfig

}


@client.event
@asyncio.coroutine
def on_ready():
    print('Bot is logged in successfully. Running on servers:\n')
    for s in client.servers:
        print(" - %s (%s)" % (s.name, s.id))

    for member in client.get_all_members():
        if member.status == discord.Status.online:
            onlinetime_manager.set_join_time(member.id)

    yield from client.change_presence(game=Game(name="v0.3"))



@client.event
@asyncio.coroutine
def on_message(message):
    if message.content.startswith(STATICS.PREFIX):
        invoke = message.content[len(STATICS.PREFIX):].split(" ")[0]
        args = message.content.split(" ")[1:]
        print("Command from %s: INVOKE: %s; ARGS: %s" % (message.author, invoke, args.__str__()[1:-1].replace("'", "")))

        if commands.__contains__(invoke):
            yield from commands.get(invoke).ex(message, invoke, args, client)
        else:
            yield from client.send_message(message.channel, embed=Embed(color=discord.Color.red(), description=("There is no such command: %s" % invoke)))


@client.event
async def on_member_update(before, after):

    await onlinetime_manager.ex(before, after)

    if after.game is not None:
        await role_manager.ex(after, client)


@client.event
async def on_voice_state_update(before, after):
    # Clear textchannel 'musicbot' when Rythm leaves voice channel
    if after.id == '235088799074484224':
        if after.voice.voice_channel is None and before.voice.voice_channel is not None:
            channel = discord.utils.get(after.server.channels, name="musicbot")
            await client.purge_from(channel, limit=100, check=is_not_pinned)


def is_not_pinned(m):
    return not m.pinned


access_token = os.environ.get('ACCESS_TOKEN')
if access_token is not None:
    client.run(access_token)
else:
    print("No Token found! Bot is not running!")
