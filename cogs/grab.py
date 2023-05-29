#!/usr/bin/env python3

from discord.ext import commands
import discord.utils
import yaml
import os
import random

# Metadata

NAME        = 'grab'
GRAB_BRIEF       = "Grab the last message from a user"
GRAB_USAGE       = '''Usage: !grab <mention>'''
GRAB_DESCRIPTION = '''This grabs the last message from a given mention. You can then look at what has been grabbed for a mention using agrab and rgrab.
Ex usage:
!grab @luke
> Grabbed: @luke: I hate women!'''

AGRAB_BRIEF       = "Display ALL grabbed messages from a user"
AGRAB_USAGE       = '''Usage: !agrab <mention>'''
AGRAB_DESCRIPTION = '''This displays ALL grabbed messages from a mention. You can add to the grabbed messages using !grab.
Ex usage:
!agrab @luke
> @luke: I hate women!
> @luke: Oopsie woopsie, I made a fucky wucky!
> @luke: I like sucking'''

RGRAB_BRIEF       = "Display a random grabbed message from a user"
RGRAB_USAGE       = '''Usage: !rgrab <mention>'''
RGRAB_DESCRIPTION = '''This displays a random grabbed messages from a mention. You can add to the grabbed messages using !grab.
Ex usage:
!rgrab @luke
> @luke: I like sucking'''



# Cog Declaration
class GrabCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "checkpoints")
        self.ckpt_path = os.path.join(self.base_path, "grab.yaml")
        self.log_path = os.path.join(self.base_path, "grab.log")
        self.log_count = 0

        if not os.path.isdir(self.base_path):
            os.mkdir(self.base_path)

        if not os.path.isfile(self.ckpt_path):
            open(self.ckpt_path, 'x')

        if not os.path.isfile(self.log_path):
            open(self.log_path, 'x')

        with open(self.ckpt_path, "r+") as fd:
            self.grabs = yaml.safe_load(fd)

        if not self.grabs:
            self.grabs = dict()

        self.log_fd = open(self.log_path, "r+")

        self.read_log()




    def write_txn(self, txn):
        write_dict = {"author": txn[0], "msg": txn[1]}
        self.log_fd.write("BEGIN_TRANSACTION\n" + yaml.dump(write_dict) + "END_TRANSACTION\n")
        self.log_fd.flush()
        os.fsync(self.log_fd.fileno())
        self.log_count += 1

        if txn[0] not in self.grabs:
            self.grabs[txn[0]] = set()

        self.grabs[txn[0]].add(txn[1])

        if self.log_count > 25:
            self.write_checkpoint()

    def write_checkpoint(self):
        with open(f"{self.ckpt_path}.bkp", "w+") as ckpt_fd:
            yaml.dump(self.grabs, ckpt_fd)

        os.rename(f"{self.ckpt_path}.bkp", self.ckpt_path)
        os.truncate(self.log_fd.fileno(), 0)
        self.log_count = 0

    def read_log(self):
        curr_txn = ''
        for line in self.log_fd:
            if line.startswith("BEGIN_TRANSACTION"):
                self.log_count += 1
                curr_txn = ''
            elif line.startswith("END_TRANSACTION"):
                try:
                    txn = yaml.safe_load(curr_txn)
                    if txn["author"] not in self.grabs:
                        self.grabs[txn["author"]] = set()

                    self.grabs[txn["author"]].add(txn["msg"])
                except yaml.YAMLError as exp:
                    print(f"Error parsing transaction: {exp}")
                except Exception as e:
                    print(e)
            else:
                curr_txn += line

    @commands.command(name=NAME, aliases=[], pass_context=True, brief=GRAB_BRIEF, help=GRAB_USAGE, description=GRAB_DESCRIPTION)
    async def grab(self, ctx, *, chnl_msg):
        author = ''
        message = await  discord.utils.find(lambda m: (m.author.mention == chnl_msg and not m.content.startswith("!grab")), ctx.channel.history(limit=200))
        if message is None:
            return # couldn't find message with author

        phrase = message.content
        author = message.author.mention

        self.write_txn((author, phrase))

        await ctx.send(f"Grabbed: {author}: {phrase}")

    @commands.command(name=f'a{NAME}', aliases=[], pass_context=True, brief=AGRAB_BRIEF, help=AGRAB_USAGE, description=AGRAB_DESCRIPTION)
    async def agrab(self, ctx, *, chnl_msg):
        await ctx.send(f"Displaying all grabs for {chnl_msg}")
        for message in self.grabs.get(chnl_msg, []):
            await ctx.send(f"{chnl_msg}: {message}")


    @commands.command(name=f'r{NAME}', aliases=[], pass_context=True, brief=RGRAB_BRIEF, help=RGRAB_USAGE, description=RGRAB_DESCRIPTION)
    async def rgrab(self, ctx, *, chnl_msg):
        message = random.choice(list(self.grabs.get(chnl_msg, [])))
        await ctx.send(f"{chnl_msg}: {message}")

# Register

async def setup(client):
    await client.add_cog(GrabCog(client))
