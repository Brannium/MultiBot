import time

import discord

from utility import StatsManager

sm = StatsManager
join_time = {}


async def ex(before, after):

    # User went online
    if not before.status == discord.Status.online and after.status == discord.Status.online:
        set_join_time(after.id)
    # User went offline/afk
    elif before.status == discord.Status.online and not after.status == discord.Status.online:
        save_time(after)


def set_join_time(member_id):

    join_time[member_id] = time.time()
    print('%s: %s' % (member_id, join_time[member_id]))


def save_time(member):

    stats = sm.getStats(member.server)
    if member.id in stats['onlinetime']:
        stats['onlinetime'][member.id] += (time.time() - join_time[member.id])
    else:
        stats['onlinetime'][member.id] = time.time() - join_time[member.id]
    sm.saveStats(member.server, stats)
    del join_time[member.id]
