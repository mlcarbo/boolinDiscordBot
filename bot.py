#!/usr/bin/env python3

import discord
from discord.ext import commands
import dotenv
import os
import sys
import logging
import random
import glob
dotenv.load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

#bot = commands.Bot(command_prefix="!", description="Bot for booling discord chat", intents=intents)

class Client(commands.Bot):
    def __init__(self, command_prefix=commands.when_mentioned_or("!"), description="Bot for booling discord chat", intents=discord.Intents.default()):
        intents.members = True
        intents.message_content = True

        super().__init__(command_prefix=command_prefix, intents=intents, description=description)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


    async def setup_hook(self):
        await self.load_cogs()

    async def load_cogs(self, cogs_dir = None):
        #importlib
        cogs_root = os.path.dirname(__file__)
        cogs_dir  = cogs_dir or os.path.join(cogs_root, "cogs")

        if not cogs_root in sys.path:
            sys.path.insert(0, cogs_root)

        for cog_path in glob.glob(f"{cogs_dir}/*.py"):
            cog_name = cog_path.replace(cogs_root + "/", "")
            cog_name = cog_name[:-3].replace('/', ".")

            if cog_name.endswith('__'):
                continue
            if cog_name in self.extensions:
                await self.reload_extension(cog_name)
            else:
                await self.load_extension(cog_name)
            print(cog_name)



client = Client()

@client.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split("d"))
    except Exception:
        await ctx.send("Format has to be in NdN!")
        return

    result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))

    await ctx.send(result)

@client.command(aliases=["unifo", "whois"])
async def user_info(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    roles = [role.mention for role in member.roles]
    embed = discord.Embed(title="Member info", description=f"Here's the info on the user {member.mention}", color=discord.Color.dark_purple(), timestamp=ctx.message.created_at)
    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name="ID", value = member.id)
    embed.add_field(name="Name", value = f'{member.name}#{member.discriminator}')
    embed.add_field(name="Nickname", value = f'{member.display_name}')
    embed.add_field(name="Status", value = f'{member.status}')
    embed.add_field(name="Created at", value = member.created_at.strftime("%a, %B %#d, %Y, %I:%M %p "))
    embed.add_field(name="Joined at", value = member.joined_at.strftime("%a, %B %#d, %Y, %I:%M %p "))
    embed.add_field(name=f"Roles ({len(roles)-1})", value = " ".join(roles[1:]))
    embed.add_field(name=f"Top Role", value = member.top_role.mention)
    await ctx.send(embed=embed)

@client.command(aliases=["stop"])
async def shutdown(ctx):
    await client.close()

@client.command(aliases=["rr"])
async def reload(ctx):
    await client.load_cogs()

#load_modules(bot)

client.run(os.environ['DISCORD_TOKEN'])#, log_handler=handler, log_level=logging.DEBUG)
