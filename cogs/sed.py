#!/usr/bin/env python3
import re
from discord.ext import commands

# Metadata

NAME    = 'sed'
ENABLE  = True
PATTERN = '^[s]?/([^/]+)/([^/]*)[/]*$'
USAGE   = '''Usage: s/pattern/replacement/'''
DESCRIPTION = '''This searches the channel's history for the most recent line that has the
pattern and then performs the replacement.
'''

# Cog
class SedCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="sed replacement like in linux", help=USAGE, description=DESCRIPTION)
    async def sed(self, ctx, *, message):
        if not re.search(PATTERN, message):
            return
        _, pattern, replacement, *_ = message.split("/")
        async for original in ctx.channel.history(limit=200):
            if re.search(PATTERN, original.content) or original.content.startswith("!sed "):
                continue
            if not re.search(pattern, original.content):
                continue
            replaced = re.sub(pattern, replacement, original.content)
            await ctx.send(f"{ctx.message.author.mention}: {replaced}")
            return

# Register
async def setup(client):
    await client.add_cog(SedCog(client))
