#!/usr/bin/env python3

import random

from discord.ext import commands

# Metadata

NAME    = 'leetspeak'
ENABLE  = True
PATTERN = '^!leet (?P<phrase>.*)'
USAGE   = '''Usage: !leet <phrase>'''
DESCRIPTION = '''Given a phrase, this translates the phrase into leetspeak.
Example:
    > !leet notre dame
    n07r3 d4m3
'''

# Constants

# Mapping from http://en.wikipedia.org/wiki/Leet

_A = ('a', '4', '4', '@', '@')
_C = ('c', 'c', 'c', '(', '<')
_E = ('e', '3', '3', '3')
_L = ('l', '1', '1', '1', '|')
_O = ('o', '0', '0', '0', '()')
_S = ('s', '5', '5', '$', 'z')
_T = ('t', '7', '+', '7', '+')

# Cog
class LeetCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["leet", "133t"], pass_context=True, brief="replace text with leetspeek", help=USAGE, description=DESCRIPTION)
    async def leetspeak(self, ctx, *, message = ""):
        response = message.lower().strip()\
                        .replace('a', random.choice(_A))\
                        .replace('c', random.choice(_C))\
                        .replace('e', random.choice(_E))\
                        .replace('l', random.choice(_L))\
                        .replace('o', random.choice(_O))\
                        .replace('s', random.choice(_S))\
                        .replace('t', random.choice(_T))
        await ctx.send(response)

# Register

async def setup(client):
    await client.add_cog(LeetCog(client))
