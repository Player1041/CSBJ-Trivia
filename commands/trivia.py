import disnake
from disnake.ext import tasks, commands
import random
import os
from dotenv import load_dotenv
import asyncpg

class trivia1(commands.Cog):
    
    load_dotenv('../')
    
    def __init__(self, bot = commands.Bot):
        self.bot = bot
    
    @commands.slash_command()
    async def trivia1(self, inter, questions: commands.Range[1,10] = 1):
        
        dbURL = os.environ['dbURL']
        db = await asyncpg.connect(dsn = dbURL)
        
        count = 0 #questions complete
        question = random.randint(1,8) #key/question number
        used = [] #done questions in this round
        while count != questions:
            
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
            
            if question not in used: #if question hadnt been used before
                count = count + 1 #so questions match the total requested
                embed = disnake.Embed(
                    title = f"Question {count} / {questions}",
                    description = data[0]['question']
                    )
                
                await inter.response.send_message(embed = embed, components = components)

        await db.close()
"""
    @commands.Cog.listener("on_button_click")
    async def triviaX(self, inter):

       

        if inter.author == inter.component.interaction.user:
            if inter.component.custom_id == "right":
                embed = disnake.Embed(
                title = "Right",
                description = data[0]['response']
                )

                inter.response.edit_message(embed = embed, components = None)
            
                
            
        await db.close()
       """
def setup(bot):
    bot.add_cog(trivia1(bot))
    print("Loaded Trivia")