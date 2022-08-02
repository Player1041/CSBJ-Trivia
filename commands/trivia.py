import disnake
from disnake.ext import tasks, commands
import random

class trivia(commands.Cog):

    def __init__(self, bot = commands.Bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(trivia(bot))
    print("Loaded Trivia")