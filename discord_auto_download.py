import os
# from datetime import timezone
from datetime import timedelta
import discord
import aiohttp
import aiofiles
from rashomon_screenshot_parse import parse_screenshot

CHANNEL = "rashoumon-raid"
USER = "solution"
OUTPUT_FILE = "parsed_hp.csv"

client = discord.Client()

with open("discord_api_token.txt") as f:
    discord_api_token = f.read().strip()
if not os.path.exists("screenshots"):
    os.mkdir("screenshots")


async def download_raid_screenshots(time, user, url, file_name):
    print(f"{time:%Y-%m-%d %H:%M:%S}|{user}|{url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                async with aiofiles.open(f"screenshots/{file_name}", mode="wb") as file:
                    await file.write(content)
                    await file.flush()
                ocr_output = parse_screenshot(f"screenshots/{file_name}")
                # ocr_output = parse_screenshot(bytearray(content))
                with open(OUTPUT_FILE, "a") as output_text:
                    output_text.write(f"{time},{ocr_output},{url}\n")
                os.remove(f"screenshots/{file_name}")


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    user = str(message.author.display_name)
    if user == "Cereal" or str(message.channel.name) == CHANNEL:
        if message.attachments:
            # time = message.created_at.replace(tzinfo=timezone.utc).astimezone(tz=None)
            # if user == USER:
            created_time = message.created_at + timedelta(hours=-7)
            file_name = f"Screenshot_{created_time:%Y%m%d-%H%M%S}.png"
            for attachment in message.attachments:
                await download_raid_screenshots(created_time, user, attachment.url, file_name)

client.run(discord_api_token)
