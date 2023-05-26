#!/usr/bin/env python3
# emojify.py
# Author: Matthew Carbonaro
# Inspired by https://emojify.net/ by Mark Farnum and bobbit emojify.py module by Evan Day

import random
from discord.ext import commands

import requests

# Metadata

NAME    = 'emojify'
ENABLE  = True
PATTERN = r'^!emojify\s*(?P<flag>-[a-zA-Z]+)?\s*(?P<arg>.*)$'
USAGE   = '''Usage: !emojify [<nick>|-p <phrase>] [-h]'''
DESCRIPTION = '''emojify takes the most recent message and adds emojis to it
    [optional]
    - you can specify the nick of a certain user to emoijfy their most recent message
    - you can use the -p flag to specify your own message
Examples:
    >>> !emojify
    can 🏃🏽‍♂️🏃🏽‍♂️🏃🏽‍♂️ you 👈 push ❗🏽 the branch 🌳 to github?
    >>> !emojify Danielle Croft
    Hey 😡 guys 👨😇👍 don't forget 👋🏾 to periodically check ☑️ in 💘😜 on 🔛 your 👉
    open 😰 pull 💦✊✊😤😣💦🐙 requests! Oftentimes we 👩‍👩‍👦‍👦 will 🙏👊 leave 👎🛫
    comments on ☹️ how 🤐 to fix/improve your 👉👩🏿 programs 📺 so make 👸📓 sure 👍👍🏻
    to keep 🏃‍♀️🏃‍♀️🏃‍♀️🏃‍♀️ an eye 😍 on ⬇️ that!
    >>> !emojify -p A computer once beat me at chess, but it was no match for me at kick boxing.
    A computer 👩‍💻 once 🔂 beat 🥊🍑 me 😐 at chess, but 🤔 it was no 🚫❌ match 🔥 for 😘
    me 🙋 at kick 👞 boxing.
'''

# Globals

EMOJI_TABLE_URL = 'https://raw.githubusercontent.com/farkmarnum/emojify/main/src/data/emoji-data.json'
COMMON_WORDS = set([
  'a',
  'an',
  'as',
  'is',
  'if',
  'of',
  'the',
  'it',
  'its',
  'or',
  'are',
  'this',
  'with',
  'so',
  'to',
  'at',
  'was',
  'and',
])

FLAGS = ['-p','-h']

# Cog
class EmojiCog(commands.Cog):
    def get_emoji_match(self, emoji_table: dict, word: str):
        word = ''.join(let for let in word.strip().lower() if let.isalpha())

        if word in COMMON_WORDS:
            return None

        if word not in emoji_table:
            return None

        matches: dict = emoji_table[word]

        options = list(matches.keys())
        weights = map(float, matches.values())

        return random.choices(options, weights, k=1)[0]

    def add_emojis(self, text: str, emoji_table):
        result = ''

        for word in text.split():
            result += f'{word} '

            if emoji := self.get_emoji_match(emoji_table, word):
                result += f'{emoji} '

        return result.strip()

    @commands.command(aliases=["emo"], pass_context=True, brief="emojify a phrase or a user's last message", help=USAGE, description=DESCRIPTION)
    async def emojify(self, ctx, *, msg):
        # check for -h or improper usage and print USAGE
        arg = ''
        flag = ""
        text = ''
        auth = None
        for word in msg.split(" "):
            if word.startswith("-"):
                flag = word
            else:
                arg += f'{word} '
        if flag == '-h' or flag and flag not in FLAGS:
            '''
            return [message.Message(
                        body    = ln,
                        nick    = bot.config.nick,
                        channel = msg.channel) for ln in USAGE.split('\n') if ln.strip()]
            '''
            return
        # parse arguments
        if not flag and not arg:
            # emojify most recent message
            try:
                msg = await anext(ctx.channel.history(limit=1))
                text = msg.content
                auth = msg.author
                print(text)
            except StopIteration:
                print('emojify: could not find any messages')
                return
        elif flag == '-p':
            # emojify the arg text
            if not arg:
                print('emojify: please specify a phrase')
                return

            text = arg
        else:
            # emojify most recent message from nick
            #target_nick = arg.split()[0]
            target = arg.strip()
            target_id = arg.strip()[2:-1]
            '''
            try:
                user = await ctx.bot.fetch_user(int(target_nick))
            except ValueError:
                print("couldn't turn uid in to int")
                return

            if user is None:
                return

            print(dir(user))
            '''

            async for msg in ctx.channel.history(limit=100):
                if str(msg.author.id) == target_id or msg.author.nick == target or msg.author.name == target:
                    if msg.content.startswith("!emo"):
                        continue
                    text = msg.content
                    auth = msg.author
                    print("found!")
                    break

            if not text:
                print("didn't find msg that matched")
                return
            print(text)

        # fetch emoji table
        try:
            with requests.get(EMOJI_TABLE_URL) as response:
                emoji_table = response.json()
        except Exception as e:
            print(f'emojify: couldn\'t parse emoji table: {e}')
            return
        body = self.add_emojis(text, emoji_table)
        if auth:
            body = f'{auth.mention}: ' + body
        await ctx.send(body)

# Register

async def setup(client):
    await client.add_cog(EmojiCog(client))
