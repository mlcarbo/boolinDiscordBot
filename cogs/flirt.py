#!/usr/bin/env python3
# flirt.py

from random import choice
from discord.ext import commands


# Metadata

NAME    = 'flirt'
ENABLE  = True
PATTERN = r'^!flirt ?(?P<nick>.*)'
USAGE   = '''Usage: !flirt <user|any string>'''
DESCRIPTION = ''' This flirts with the user specified by nick.'''

# Constants

FLIRT_PHRASES = [
    'if they made you in C, you would have a pointer to my heart. <3',
    'have you spent a lot of time working with computers? \'Cause you know how to turn me on.',
    'with all the variables in life, baby, you can be my constant. <3',
    'are you a keyboard? \'Cause you\'re my type.',
    'are we in the same class? \'Cause I\'d love to be able to access your private variables.',
    'are you my GitHub repository? \'Cause I want to commit to you.',
    'are you from Tennessee? \'Cause we should have sex.',
    'will you let me toggle your bits? <3',
    'sudo make love to me',
    'I\'d like to take you to the movies, but they don\'t let you take your own snacks.',
    'is your name Google? \'Cause you have everything I\'m searching for.',
    'if you were a fruit, you\'d be a \'fine-apple\'.',
    'if I make a spice joke, will you let me cumin you?',
    'are you breakfast? \'Cause you look like you\'re about to be the most important meal of my day.',
    'are you a pirate? \'Cause you put the curvy in scurvy.',
    'is your phone in your back pocket? \'Cause your ass is calling me.',
    'are you a communist? \'Cause I feel an uprising in my lower class.',
    'I may not be Fred Flintstone, but I\'ll make your bed rock.',
    'I\'ll put my basilisk in your Chamber of Secrets.',
    'your outfit is nice, but it would look better on my bedroom floor.',
    'if you\'re feeling down, I can feel you up.',
    'are you my Systems Programming homework? \'Cause I\'m not doing you, but I definitely should be.',
    'treat me like a pirate and give me that booty.',
    'are you a drill sergeant? \'Cause you have my privates standing at attention.',
    'let\'s play Titanic. You\'ll be the iceberg, and I\'ll go down.',
    'you make me horny. That\'s it.',
    'I wouldn\'t mind checking you for ticks.',
    'I\'m not a dentist, but I could give you a filling.'
]

# Command
class FlirtCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="module that will flirt with a given user", help=USAGE, description=DESCRIPTION)
    async def flirt(self, ctx, nick=None):
        body        = f'{choice(FLIRT_PHRASES)}'
        nick        = nick if nick else ctx.message.author.mention

        await ctx.send(f'{nick} {body}')
# Register

async def setup(client):
    await client.add_cog(FlirtCog(client))
