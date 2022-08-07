import disnake

from disnake.ext import tasks, commands

import random
import os
from dotenv import load_dotenv
import asyncpg
import dataclasses

@dataclasses.dataclass
class GameState:
    count: int
    used: list[int]
    user: int
    correct: str
    components: list[str]
    channel: int
    

class trivia(commands.Cog):
    
    load_dotenv('../')
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.game = {}
    
    @commands.slash_command()
    async def trivia(self, inter, questions: commands.Range[1,10] = 1):
        dbURL = os.environ['dbURL']
        
        db = await asyncpg.connect(dsn = dbURL)
     
        question = random.randint(1,10)
        
        data = await db.fetch(f"select * from trivia where key = {question}")
        
        
        right = disnake.ui.Button(label = data[0]['answer'], custom_id = 'right')

        wrong1 = disnake.ui.Button(label = data[0]['wrong1'], custom_id = 'wrong1')

        components = [right, wrong1]

        if data[0]['wrong2'] != None:
            wrong2 = disnake.ui.Button(label = data[0]['wrong2'], custom_id = 'wrong2') 
            components.append(wrong2)

        if data[0]['wrong3'] != None:
            wrong3 = disnake.ui.Button(label = data[0]['wrong3'], custom_id = 'wrong3')
            components.append(wrong3)
            
        for x in range(3):
            random.shuffle(components)
        
        gs = GameState(count = 1, used = [], user = inter.user.id, correct = data[0]['answer'], components = components, channel = inter.channel.id)
        
        if inter.user.id in self.game:
            await inter.response.send_message("You have a game going at the minute.", ephemeral = True)
            return

        else:
            embed = disnake.Embed(
                title = f"Question {gs.count} / {questions}",
                description = data[0]['question']
                )
            await inter.response.send_message(embed = embed, components = components)
            
    @commands.Cog.listener("on_button_click")
    async def triviab(self, inter):
        if inter.author == inter.message.interaction.user:
            if inter.component.custom_id == "right":
                print("right")
                await inter.response.send_message("yes")
            elif inter.component.custom_id != "right":
                print("wrong")
                await inter.response.send_message("wrong")


def setup(bot):
    bot.add_cog(trivia(bot))
    print("Loaded Trivia v2")