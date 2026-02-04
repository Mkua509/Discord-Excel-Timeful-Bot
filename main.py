import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import gspread

# Loads env file for key
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# For logging errors
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Specify the intents that you want to activate (Need to do this manually)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Connect the google spread sheet
gc = gspread.service_account(filename='service_account.json')
sh = gc.open("test")

worksheet = sh.worksheet("Sheet1")

# Set the command for the bot as !
bot = commands.Bot(command_prefix='!', intents=intents)

# Definition of the secret role in discord
secret_role = "test"

@bot.event
async def on_ready():
    print(f"We are ready to go in {bot.user.name}")

@bot.command()
async def filled_form(ctx):
    # Fetch fresh data from spreadsheet each time
    values_list = worksheet.col_values(1)
    completed_list = worksheet.col_values(2)
    discord_id = worksheet.col_values(3)
    
    # Remove headers
    values_list.pop(0)
    completed_list.pop(0)
    discord_id.pop(0)

    # Uses Zip to ensure it doesn't over iterate
    for values_list, completed_list, discord_id in zip(values_list, completed_list, discord_id):
        if completed_list == 'FALSE':
            user_id = int(discord_id)
            #await ctx.send(f"<@{user_id}> Please fill out the form :((") old comment for sending in serer
            user = await bot.fetch_user(user_id)
            await user.send(f"Please fill out the form :((")
    
    await ctx.send("DMs sent to everyone who hasn't filled the form!")

    # Allows the bot to continue processing the other commands
    await bot.process_commands(filled_form)


@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"you said {msg}")

@bot.command()
async def reply1(ctx):
    await ctx.reply("This is a reply to your message")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)