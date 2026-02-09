# About This Project:
This project is a reflection of my time in university clubs, sometimes its very difficult to track and get people to fill out [Timeful's](https://timeful.app/) and Google Sheets. Soooo I have resorted in making a discord bot that spam dm's you at certain time's of the day so that I can automate the process.

If I were to say it in a more professional way its a Discord bot that automate's availability collection for clubs by integrating spreadsheet data and user messaging, reducing manual follow ups. Pretty neat huh.

Hopefully they don't mute the bot hahahhahahaha.

## How It's Made:

**Tech used:** Python (atm but will have to implement web functions for Timeful implementations)

Currently all the bot does is connect to a excel spread sheet of the user's choosing and scan three columns: 

- Name: Name of the person
- DiscordID: Discord ID of the person in order to direct message them 
- Filled: Column with tick boxes if the box is not ticked it will send a DM to the person when command is run

There are two existing commands:

1. !filled_form: Sends out discord DM via bot to users who have not ticked the filled column inside the spread sheet
2. !time_interval (seconds): Creates a loop which periodically sends dm's based off seconds

## DISCLAIMER:

This project is currently extremely bare bones, it has only the very bare minimum and requires a very simple understanding of coding to tweak to specific sheets, but in the future I want to make it as user friendly as possible.