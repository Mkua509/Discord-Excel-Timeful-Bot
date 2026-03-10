import logging
from utils.sheets import get_worksheet
from config.config import FORMS
import asyncio

# Reminds people based on a loop
async def reminder_loop_logic(bot):

    for excel_name, sheet_name in FORMS:

        worksheet = get_worksheet(excel_name, sheet_name)
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