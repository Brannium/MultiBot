import discord

from utility import ConfigManager

cm = ConfigManager

async def ex(client, before, after):

    config = ConfigManager.getConfig(after.server)["autoclear"]

    if config["enabled"]:
        print('enabled')
        for channel_id, user_id in config["links"].items():
            if user_id == after.id:
                print('userid')
                if after.voice.voice_channel is None and before.voice.voice_channel is not None:
                    channel = discord.utils.get(after.server.channels, id=channel_id)
                    print('Clearing channel %s as %s left the voice channel' % (channel.name, user_id))
                    await client.purge_from(channel, limit=100, check=is_not_pinned)


def is_not_pinned(m):
    return not m.pinned
