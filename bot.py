import discord
import requests
from bs4 import BeautifulSoup
import asyncio
import os

TOKEN = os.getenv("TOKEN")

URL = "https://craftersmc.wiki.gg/wiki/CraftersMC_SkyBlock_Wiki"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def fetch_timer():
    response = requests.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        timer_element = soup.select_one("table:nth-of-type(2) tr td:nth-of-type(2) span:nth-of-type(2)")
        return timer_element.text if timer_element else "Timer not found"
    return "Failed to fetch data"

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    channel = discord.utils.get(client.get_all_channels(), name="1344375338008055910")
    while True:
        timer = await fetch_timer()
        if channel:
            await channel.send(f"Current Timer: {timer}")
        await asyncio.sleep(60)  # Fetch every minute

client.run(TOKEN)
