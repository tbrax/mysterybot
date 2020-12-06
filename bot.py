
#.\env\Scripts\activate

# bot.py
import os
import asyncio
import string
import discord
from dotenv import load_dotenv
from mystery import MysteryClass
from maincharacter.character import Character


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

mystery = MysteryClass()


def setupMystery():
    mystery.setupMystery()


def addMysteryCharacter(aut):
    return mystery.addDiscordAuthor(aut)


def startMystery():
    mystery.startMystery()


def mysteryParticipants():
    return mystery.getParticipantString()


def cancelMystery():
    mystery.cancelMystery()


prefix = "!"


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    isDM = False
    if not message.guild:
        isDM = True

    if (not isDM):
        if not (msg.startswith(prefix)):
            return

    if msg.startswith(prefix):
        msg = msg[len(prefix):]

    if msg.startswith("setup"):
        setupMystery()
        await message.channel.send("Setting up mystery. Use !joinmystery to become a participent.")
        # await asyncio.sleep(20)
        # await message.channel.send("Is currently " + savedvar)

    elif msg.startswith("start"):
        if (mystery.stage == 1):
            startMystery()
            autList = mystery.getCharacterList()
            for a in autList:
                usr = a.getDiscordAuth()
                startmess = a.getInfoString()
                try:
                    await usr.send(startmess)
                except:
                    print("Unsuccessfully DMed users, try again later.")
        else:
            await message.channel.send("No game in progress. Use !setup for new game.")
        # msgcon = "The mystery has started! The participents are: \n"                
        # await message.channel.send(msgcon + mysteryParticipants())

    elif msg.startswith("cancel"):
        await message.channel.send("The mystery has been canceled.")

    elif msg.startswith("joinmystery"):
        if (mystery.acceptingCharacters()):
            add = addMysteryCharacter(message.author)

            if (add == 0):
                await message.channel.send("{0} already in game".format(message.author))
            elif (add == 1):
                await message.channel.send("Added {0} to game".format(message.author))
        else:
            if (mystery.stage == 0):
                await message.channel.send("No game in progress. Use !start for new game.")
            elif mystery.stage == 2:
                await message.channel.send("Game in progress. Cannot add new participents.")
    else:
        if isDM:
            if msg.startswith(prefix):
                msg = msg[len(prefix):]

            if mystery.getStage() == 2:
                resp = mystery.useAbility(msg, message.author)
                if resp != 0:
                    message.author.send(resp)

client.run(TOKEN)
