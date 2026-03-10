from discord.ext import commands
import asyncio
import logging
from utils.reminders import reminder_loop_logic
from utils.sheets import get_worksheet
from config.config import FORMS

is_paused = False
current_loop_task = None
current_interval = None


def setup_commands(bot):

    @bot.command()
    async def time_interval(ctx, interval:int):

        global current_loop_task

        if interval < 30 or interval > 86400:
            await ctx.send("Interval must be within 30 seconds or 24 hours! Automatically set to closer value")
            interval = max(30, min(interval, 86400))

        if current_loop_task and not current_loop_task.done():
            current_loop_task.cancel()

        await ctx.send(f"Setting reminder loop interval to {interval} seconds")

        async def loop_task():
            while True:
                if not is_paused:
                    await reminder_loop_logic(bot)
                await asyncio.sleep(interval)

        current_loop_task = asyncio.create_task(loop_task())


    @bot.command()
    async def filled_form(ctx):

        for excel_name, sheet_name in FORMS:
            worksheet = get_worksheet(excel_name, sheet_name)

            values_list = worksheet.col_values(1)
            completed_list = worksheet.col_values(2)
            discord_id = worksheet.col_values(3)

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


    @bot.command()
    async def stop_reminders(ctx):

        global current_loop_task
        global is_paused

        if current_loop_task is not None:
            current_loop_task.cancel()
            current_loop_task = None
            is_paused = False
            await ctx.send("Stopped the current looped task")
        else:
            await ctx.send("There is no current task!")


    @bot.command()
    async def pause_reminders(ctx):

        global is_paused

        if current_loop_task is None or current_loop_task.done():
            await ctx.send("No active reminders")
        elif is_paused:
            await ctx.send("The task is already paused!")
        else:
            is_paused = True
            await ctx.send("The looped task is now paused")


    @bot.command()
    async def resume_reminders(ctx):

        global is_paused

        if current_loop_task is None or current_loop_task.done():
            await ctx.send("No active reminders")
        elif is_paused:
            is_paused = False
            await ctx.send("The looped task is now unpaused")
        else:
            await ctx.send("The reminder is already looping!")