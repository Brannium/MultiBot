import discord

from utility import ConfigManager

cm = ConfigManager

async def ex(client, before, after):

    config = ConfigManager.getConfig(after.server)["autoclear"]

    if config["enabled"]:
        for channel_id, user_id in config["links"].items():
            if user_id == after.id:
                if after.voice.voice_channel is None and before.voice.voice_channel is not None:
                    channel = discord.utils.get(after.server.channels, id=channel_id)
                    await client.purge_from(channel, limit=100, check=is_not_pinned)


def is_not_pinned(m):
    return not m.pinned
