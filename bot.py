import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  # For slash commands

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(e)

@tree.command(name="nitro", description="Sends a fake Nitro gift message.")
async def fake_nitro(interaction: discord.Interaction):
    embed = discord.Embed(
        title="You've been gifted a subscription!",
        description="**1 month of Discord Nitro**\n\nClick the button below to accept.",
        color=0x5865F2
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/936790831748554792.png")

    button = discord.ui.Button(label="Accept", style=discord.ButtonStyle.success)

    async def button_callback(i: discord.Interaction):
        await i.response.send_message("This is a mock Nitro message for demo purposes.", ephemeral=True)

    button.callback = button_callback
    view = discord.ui.View()
    view.add_item(button)

    await interaction.response.send_message(embed=embed, view=view)
