#!/usr/bin/env python3

from discord import utils
from discord.ext import commands
from random import choice

# Metadata

NAME        = 'bully'
BRIEF       = "Module used to bully your friends"
USAGE       = '''Usage: !bully <mention | any text>'''
DESCRIPTION = '''This command will generate a random insult to bully the provided mention if it is provided, else it will just fill in what is passed'''

BULLY_PHRASES = [
    '\'s day has been ruined by your message,',
    ' wants to return to monke, but not if you\'re coming, too,',
    ' knows how much of a duck-banging degenerate you are,',
    ' hopes you order pizza from Modern Market, but then you realize you have an interview to go to that you\'re about to be late to, so you frantically rush to it before realizing it\'s over Zoom, so you pull out your laptop and search through your email, but can\'t find the link, before finally discovering it 2 whole minutes later, making you late to your interview, which you fail by the way, after which you remember you ordered pizza which, even though cold, would still be enough to lift your spirits up a little, except you find it was taken by someone else, Modern Market has closed, and you are left with nothing but dread, disgust, and misery,',
    ' believes you\'re too incompetent to know that you\'re being bullied,',
    ' doesn\'t care about your race, sex, or age... or anything about you really,',
    ' has more maidens than you,',
    '\'s faith in society has plummeted since meeting you,',
    ' think you\'re about as good as the dining hall food,',
    ' gives eMoTiOnAL dAmAgE to',
    ' has a confession to make. You\'re ugly,',
    ' thinks you\'re so ugly that when your mom dropped you off at school she got a fine for littering, ',
    ' thinks your brain is so tiny that you\'d have to stand on a penny to see over it, ',
    ' thinks that you must have been born on a highway, since that\'s where most accidents happen, ',
    ' heard that you\'re so dumb, you thought a quarterback was a refund, ',
    ' would like to see things from your point of view, but can\'t seem to get their head that far up your butt, ',
    ' thinks that your family tree must be a cactus because everyone on it is a prick, ',
    ' thinks that if laughter is the best medicine, your face must be curing the world, ',
    ' thinks that you\'re so ugly, you scared the crap out of the toilet, ',
    ' isn\'t saying you\'re stupid, they\'re just saying you\'ve got bad luck when it comes to thinking, ',
    ' heard you got a brain transplant and the brain rejected you, ',
]

# Cog Declaration
class BullyCog(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(name=NAME, aliases=[], pass_context=True, brief=BRIEF, help=USAGE, description=DESCRIPTION)
    async def bully(self, ctx, *, user):
        """Provide Functionality"""
        await ctx.send(f'{ctx.message.author.mention} {choice(BULLY_PHRASES)} {user}')


# Register

async def setup(client):
    await client.add_cog(BullyCog(client))
