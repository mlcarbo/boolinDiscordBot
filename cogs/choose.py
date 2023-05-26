#!/usr/bin/env python3
# choose.py

import random

from discord.ext import commands

# Metadata

NAME    = 'choose'
ENABLE  = True
PATTERN = '^!choose (?P<options>.*)'
USAGE   = '''Usage: !choose <options>'''
DESCRIPTION = '''Given a list of options separated by "or", this chooses one of them.
Example:
    > !choose stay or go
    stay
'''

# Cog
class ChooseCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="module that randomly chooses an option", help=USAGE, description=DESCRIPTION)
    async def choose(self, ctx, *, options):
        if not options:
            return
        options = options.split(' or ')
        await ctx.send(random.choice(options))


# Register
async def setup(client):
    await client.add_cog(ChooseCog(client))

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
