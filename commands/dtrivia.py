import disnake
from disnake.ext import tasks, commands
import random

class dTrivia(commands.Cog):

    def __init__(self, bot = commands.Bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(dTrivia(bot))
    print("Loaded Daily Trivia")