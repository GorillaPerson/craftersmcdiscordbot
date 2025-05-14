import random
import string
import discord
import os
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- KEY GENERATORS ---

def generate_division_key():
    # Format: XXXX-XXXX-XXXX-XXXX (uppercase letters and digits)
    return '-'.join(
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        for _ in range(4)
    )

def generate_disconnect_key():
    # Format: xxxxxxxxxx-xxxxxxxxxx-RustEXT (lowercase hex)
    part1 = ''.join(random.choices('0123456789abcdef', k=10))
    part2 = ''.join(random.choices('0123456789abcdef', k=10))
    return f"{part1}-{part2}-RustEXT"

# Map of available key types
key_generators = {
    "division": generate_division_key,
    "disconnect": generate_disconnect_key
}

# --- BOT EVENTS & COMMANDS ---

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print("Error syncing commands:", e)

@bot.tree.command(name="generatekey", description="Generate random keys")
@app_commands.describe(name="Key type (like division or disconnect)", amount="Number of keys to generate")
async def generatekey(interaction: discord.Interaction, name: str, amount: int):
    allowed_channel_id = 1372287750396575876  # Only allow this channel

    if interaction.channel_id != allowed_channel_id:
        await interaction.response.send_message(
            "This command can only be used in the designated keygen channel.",
            ephemeral=True
        )
        return

    name = name.lower()

    if name not in key_generators:
        await interaction.response.send_message(
            f"Invalid key name. Currently supported: {', '.join(key_generators.keys())}",
            ephemeral=True
        )
        return

    if amount > 20:
        await interaction.response.send_message("Please generate 20 or fewer keys at once.", ephemeral=True)
        return

    generate = key_generators[name]
    keys = [generate() for _ in range(amount)]
    key_list = '\n'.join(keys)

    embed = discord.Embed(
        title=f"{name.capitalize()} - Generated Keys",
        description=f"```{key_list}```",
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Requested by {interaction.user.name}")

    await interaction.response.send_message(embed=embed, ephemeral=True)

# --- RUN THE BOT ---
bot.run(os.environ["DISCORD_TOKEN"])
