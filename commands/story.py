import disnake
from disnake.ext import tasks, commands
import random

class story(commands.Cog):

    def __init__(self, bot = commands.Bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(story(bot))
    print("Loaded Story Mode")