import random
import string
import discord
import os
import io
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- KEY GENERATORS ---

def generate_division_key():
    return '-'.join(
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        for _ in range(4)
    )

def generate_disconnect_key():
    part1 = ''.join(random.choices('0123456789abcdef', k=10))
    part2 = ''.join(random.choices('0123456789abcdef', k=10))
    return f"{part1}-{part2}-RustEXT"

def generate_r6ua_key():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=24))

key_generators = {
    "division": generate_division_key,
    "disconnect": generate_disconnect_key,
    "r6ua": generate_r6ua_key
}

# --- BOT EVENTS ---

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print("Error syncing commands:", e)

# --- SLASH COMMAND ---

@bot.tree.command(name="generatekey", description="Generate random keys")
@app_commands.describe(name="Key type (like division, disconnect, or r6ua)", amount="Number of keys to generate")
async def generatekey(interaction: discord.Interaction, name: str, amount: int):
    allowed_channel_id = 1372287750396575876
    privileged_role_id = 1372362345568800788  # Replace with your actual privileged role ID

    if interaction.channel_id != allowed_channel_id:
        await interaction.response.send_message(
            "This command can only be used in the designated keygen channel.",
            ephemeral=True
        )
        return

    name = name.lower()

    if name not in key_generators:
        await interaction.response.send_message(
            f"Invalid key name. Supported: {', '.join(key_generators.keys())}",
            ephemeral=True
        )
        return

    # Check if user has the privileged role
    member = interaction.user  # This is a Member object
    has_privileged_role = any(role.id == privileged_role_id for role in member.roles)

    max_keys = 1000 if has_privileged_role else 20

    if amount > max_keys:
        await interaction.response.send_message(
            f"You can generate up to {max_keys} keys.",
            ephemeral=True
        )
        return

    # Generate keys
    generate = key_generators[name]
    keys = [generate() for _ in range(amount)]
    key_list = '\n'.join(keys)

    # Private embed with keys
    private_embed = discord.Embed(
        title=f"{name.capitalize()} - Generated Keys",
        description=f"```{key_list}```",
        color=discord.Color.blue()
    )
    private_embed.set_footer(text=f"Requested by {interaction.user.name}")

    file = discord.File(io.StringIO(key_list), filename=f"{name}_keys.txt")

    await interaction.response.send_message(embed=private_embed, file=file, ephemeral=True)

    # Public announcement
    public_embed = discord.Embed(
        description=f"**{interaction.user.mention}** generated **{amount}** keys for **{name}**",
        color=discord.Color.green()
    )

    await interaction.channel.send(embed=public_embed)

# --- RUN BOT ---
bot.run(os.environ["DISCORD_TOKEN"])

