#!/usr/bin/env python3

from discord.ext import commands

# Metadata

NAME        = 'UPDATE NAME'
BRIEF       = "UPDATE BRIEF (DESC IN !HELP MENU)"
USAGE       = '''Usage: <HOW TO USE>>'''
DESCRIPTION = '''UPDATE DESCRIPTION'''

# Cog Declaration
### NAME COG ###
class Cog(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(name=NAME, aliases=[], pass_context=True, brief=BRIEF, help=USAGE, description=DESCRIPTION)
    async def cmdname(self, ctx, *, message):
        """Provide Functionality"""
        pass

# Register

async def setup(client):
    ### UPDATE COG NAME HERE ###
    await client.add_cog(Cog(client))
