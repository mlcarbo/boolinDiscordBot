#!/usr/bin/env python3

from discord.ext import commands
import discord.utils

# Metadata

NAME        = 'mock'
BRIEF       = "mock a user's last message or a given phrase"
USAGE       = '''Usage: !mock <phrase|mention>'''
DESCRIPTION = '''Given a phrase, this translates the phrase into a mocking spongebob phrase.
Example:
    > !mock this theory homework should be easy
    tHiS ThEoRy hOmEwOrK ShOuLd bE EaSy

Alternatively, given a mention, this translates the last message from the user
into a mocking spongebob phrase.
Example:
    > !mock @maria
    @maria: i'm nOt a fUrRy'''

# Cog Declaration
class MockCog(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(name=NAME, aliases=[], pass_context=True, brief=BRIEF, help=USAGE, description=DESCRIPTION)
    async def mock(self, ctx, *, chnl_msg):
        author = ''
        message = await  discord.utils.find(lambda m: (m.author.mention == chnl_msg and not m.content.startswith("!mock")), ctx.channel.history(limit=200))
        if message is not None:
            phrase = message.content
            author = message.author.mention
        else:
            phrase = chnl_msg

        phrase   = phrase.lower().rstrip()
        response = ''

        for count, letter in enumerate(phrase):
            if count % 2:
                letter = letter.upper()
            response += letter

        await ctx.send((f"{author}: " if author else "") + response)

# Register

async def setup(client):
    await client.add_cog(MockCog(client))
