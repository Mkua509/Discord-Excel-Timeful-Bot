import discord
import logging
from dotenv import load_dotenv
import os

# Loads env file for key
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# For logging errors
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Specify the intents that you want to activate
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Initiate excel
FORMS = {
    ("test", "Sheet1")
}
