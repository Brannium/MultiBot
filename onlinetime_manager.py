import time

import discord

import main


async def ex(before, after):
    await print(123)
    # User went online
    if not before.status == discord.Status.online and after.status == discord.Status.online:
        main.onlinetime[after.id] = time.time()
    elif before.status == discord.Status.online and not after.status == discord.Status.online:
        print(time.time() - main.onlinetime[after.id])
        del main.onlinetime[after.id]
