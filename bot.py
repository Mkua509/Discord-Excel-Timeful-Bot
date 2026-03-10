import discord
from discord.ext import commands
from config.config import token, intents, handler
from cogs.commands import setup_commands

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready my name is {bot.user.name}")

setup_commands(bot)

bot.run(token, log_handler=handler, log_level="DEBUG")