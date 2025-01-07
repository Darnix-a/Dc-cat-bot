import discord
from discord import app_commands
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

class CatBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = CatBot()

@client.tree.command(name="car", description="Get a random cat picture!")
async def cat(interaction: discord.Interaction):
    await interaction.response.defer()
    
    api_url = "https://api.thecatapi.com/v1/images/search"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                cat_url = data[0]['url']
                
                embed = discord.Embed(
                    title="🐱 Here's your random cat!",
                    color=discord.Color.blue()
                )
                embed.set_image(url=cat_url)
                
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send("Sorry, I couldn't fetch a cat picture right now! 😿")

client.run(os.getenv('DISCORD_TOKEN'))
