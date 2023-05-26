#!/usr/bin/env python3
# lenny.py

import random

from discord.ext import commands

# Metadata

NAME    = 'lenny'
ENABLE  = True
PATTERN = r'^![Ll]enny\s*(?P<text>.*)$'
USAGE   = '''Usage: !lenny [some phrase]'''
DESCRIPTION = '''Displays a Lenny face ( ͡° ͜ʖ ͡°)'''

# Lenny Faces from Gonzobot

LENNYS = [
    '( \u0361\u00B0 \u035C\u0296 \u0361\u00B0)',
    '( \u0360\u00B0 \u035F\u0296 \u0361\u00B0)',
    '\u1566( \u0361\xb0 \u035c\u0296 \u0361\xb0)\u1564',
    '( \u0361\u00B0 \u035C\u0296 \u0361\u00B0)',
    '( \u0361~ \u035C\u0296 \u0361\u00B0)',
    '( \u0361o \u035C\u0296 \u0361o)', u'\u0361\u00B0 \u035C\u0296 \u0361 -',
    '( \u0361\u0361 \u00B0 \u035C \u0296 \u0361 \u00B0)\uFEFF',
    '( \u0361 \u0361\u00B0 \u0361\u00B0  \u0296 \u0361\u00B0 \u0361\u00B0)',
    '(\u0E07 \u0360\u00B0 \u035F\u0644\u035C \u0361\u00B0)\u0E07',
    '( \u0361\u00B0 \u035C\u0296 \u0361 \u00B0)',
    '( \u0361\u00B0\u256D\u035C\u0296\u256E\u0361\u00B0 )'
]

# Command
class LennyCog(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(aliases=["sus", "Lenny"], pass_context=True, brief="displays a lenny face", help=USAGE, description=DESCRIPTION)
    async def lenny(self, ctx, *, message: str = ""):
        response = random.choice(LENNYS)
        if message:
            response += ' ' + message
        await ctx.send(response)

# Register

async def setup(client):
    await client.add_cog(LennyCog(client))
