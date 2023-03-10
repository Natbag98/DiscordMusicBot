import discord
from discord.ext import commands
import os
import asyncio

with open('token.txt') as file:
    TOKEN = file.read()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def add_cogs():
    """
    Adds all the cogs in the cogs folder to the bot
    """
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')

async def main():
    """
    Setup and run the bot.\n
    Must be run using asyncio.run()
    """
    async with bot:
        await add_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
