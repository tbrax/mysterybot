
#.\env\Scripts\activate

# bot.py
import os
import discord
import asyncio
import string
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')



savedvar = 0
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content   
    if msg == '!start':    
        await message.channel.send("Type in a var!")
        await asyncio.sleep(3)
        await message.channel.send("You choose" + savedvar)
    elif msg.contains("!var"):
        savedvar = msg[4:]
        

client.run(TOKEN)
