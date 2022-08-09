import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv
import asyncpg

class submit(commands.Cog):
    
    load_dotenv('../')
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def submit(
    self,
    inter,
    question: str,
    answer: str,
    wrong1: str,
    wrong2: str = None,
    wrong3: str = None,
    response: str = None,
    category: str = None,
    level: int = None
    ):
        dbURL = os.environ['dbURL']
        db = await asyncpg.connect(dsn = dbURL)
        data = await db.fetch('select * from trivia')
        
        acceptedIDs = [
            894709343012941927, #Player
            736820906604888096, #Hogwarts
            760426797418151937 #Korta 
            ]
        if inter.user.id in acceptedIDs:
            
            await db.execute(f'''
            insert into trivia (question, answer, wrong1, wrong2, wrong3, response, category)
            values($1, $2, $3, $4, $5, $6, $7)
            ''', question, answer, wrong1, wrong2, wrong3, response, category)
        
            data = await db.fetch('SELECT * FROM trivia WHERE key=(SELECT max(key) FROM trivia)')
            embed = disnake.Embed(
                title = "Success",
                description = f" Key - {data[0]['key']}\nQuestion - {question}\nAnswer - {answer}\nWrong 1 - {wrong1}\nWrong 2 - {wrong2}\nWrong 3 - {wrong3}\nResponse - {response}\nCategory - {category}\nLevel - {level}\n")
            await inter.response.send_message(embed = embed)
        else:
            await inter.response.send_message("You aren't allowed to do this.", ephemeral = True)
            
def setup(bot):
    bot.add_cog(submit(bot))
    print("Loaded submittion")