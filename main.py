import discord
from discord.ext import commands, tasks
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

#Initiate excel (Just change these values in correspondence to your needs)
excel_name = "test"
sheet_name = "Sheet1"

# Connect the google spread sheet
gc = gspread.service_account(filename='service_account.json')
sh = gc.open(excel_name)

worksheet = sh.worksheet(sheet_name)

# Set the command for the bot as !
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"We are ready to go in {bot.user.name}")
    reminder_loop.start()

# Reminds people based on a loop
@tasks.loop(seconds=5)
async def reminder_loop():
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
        user_id = int(discord_id)
        user = await bot.fetch_user(user_id)
        if completed_list == 'FALSE':
            await user.send(f"Please fill out the {excel_name} form :((")
    

# Reminds people based on a command
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
            await user.send(f"Please fill out the {excel_name} form :((")
    
    await ctx.send("DMs sent to everyone who hasn't filled the form!")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)