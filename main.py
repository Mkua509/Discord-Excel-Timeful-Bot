import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
import gspread
import asyncio

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

current_loop_task = None

@bot.command()
async def time_interval(ctx, interval:int):
    
    global current_loop_task
    
    # Bounds for safety
    if interval < 30 or interval > 86400:
        await ctx.send("Interval must be within 30 seconds or 24 hours! Automatically set to closer value")
        interval = max(30, min(interval, 86400))  # 30 sec → 24 hours
    

    # Stop the previous loop
    if current_loop_task and not current_loop_task.done():
        current_loop_task.cancel()
    
    await ctx.send(f"Setting reminder loop interval to {interval} seconds")

    # Start a new async task
    async def loop_task():
        while True:
            await reminder_loop_logic()
            await asyncio.sleep(interval)
    
    current_loop_task = asyncio.create_task(loop_task())


# Reminds people based on a loop
async def reminder_loop_logic():
    # Fetch fresh data from spreadsheet each time
    values_list = worksheet.col_values(1) 
    completed_list = worksheet.col_values(2)
    discord_id = worksheet.col_values(3)
    
    # Remove headers
    values_list.pop(0)
    completed_list.pop(0)
    discord_id.pop(0)

    for value, completed, user_id in zip(values_list, completed_list, discord_id):
        if completed == 'FALSE':
            try:
                user = await bot.fetch_user(int(user_id))
                await user.send(f"Please fill out the {excel_name} form :((")
            except Exception as e:
                logging.error(f"Failed DM {user_id}: {e}")

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

    for value, completed, user_id in zip(values_list, completed_list, discord_id):
        if completed == 'FALSE':
            try:
                user = await bot.fetch_user(int(user_id))
                await user.send(f"Please fill out the {excel_name} form :((")
            except Exception as e:
                logging.error(f"Failed DM {user_id}: {e}")
                
    await ctx.send("DMs sent to everyone who hasn't filled the form!")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)