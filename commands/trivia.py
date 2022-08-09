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
    response: str
    

class trivia(commands.Cog):
    
    load_dotenv('../')
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.game = {}
    
    @commands.slash_command()
    async def trivia(self, inter, question: int = None):
        
        key = (inter.guild.id, inter.user.id)
        if key in self.game:
            await inter.response.send_message("You have a game!", ephemeral = True)
        else:
            await inter.response.defer()
            dbURL = os.environ['dbURL']
            
            db = await asyncpg.connect(dsn = dbURL)
            top = await db.fetch('select count(key) from trivia')
            print(top)
            if question == None:
                question = random.randint(1,top[0]['count'])
            else:
                question = question
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
            
            self.game[key] = GameState(count = 1, used = [], user = inter.user.id, correct = data[0]['answer'], components = components, channel = inter.channel.id, response = data[0]['response'])
            
            
            embed = disnake.Embed(
                title = f"Question ",
                description = data[0]['question']
                    
                )
            await inter.edit_original_message(embed = embed, components = components)
            await db.close()
            
        
    @commands.Cog.listener("on_button_click")
    async def triviab(self, inter):
        await inter.response.defer()
        key = (inter.guild.id, inter.user.id)
        gs = self.game[key]
        dbURL = os.environ['dbURL']
    
        db = await asyncpg.connect(dsn = dbURL)
            
        data = await db.fetch(f'SELECT * FROM trivia WHERE key=(SELECT max(key) FROM trivia);')
            
        if inter.author == inter.message.interaction.user:
            embed = disnake.Embed()
            if inter.component.custom_id == "right":
                print("right")
                embed.title = "Correct!"
                embed.description = gs.response
                embed.colour = disnake.Colour.green()
                await inter.edit_original_message(
                    embed = embed, components = None
                    )
            elif inter.component.custom_id != "right":
                print("right")
                embed.title = "Wrong!"
                embed.description = f"The right answer was {gs.correct}. {gs.response}"
                embed.colour = disnake.Colour.red()
                await inter.edit_original_message(
                    embed = embed, components = None
                    )
        else:
            await inter.edit_original_message("This isn't your question.", ephemeral = True)
        del self.game[key]


def setup(bot):
    bot.add_cog(trivia(bot))
    print("Loaded Trivia v2")