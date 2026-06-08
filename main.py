import os
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="promote", description="Promote a member")
@app_commands.describe(
    user="User being promoted",
    rank="New rank",
    reason="Reason for promotion"
)
async def promote(interaction: discord.Interaction, user: discord.Member, rank: str, reason: str):

    embed = discord.Embed(
        title="🏆 Staff Promotion",
        description=(
            f"Congratulations, the High Command has decided to promote you.\n\n"
            f"• **User:** {user.mention}\n"
            f"• **Updated Rank:** {rank}\n"
            f"• **Reason:** {reason}"
        ),
        color=discord.Color.red()
    )

    embed.set_footer(text=f"Issued By {interaction.user.display_name}")

    await interaction.response.send_message(
        content=user.mention,
        embed=embed
    )

@bot.tree.command(name="infract", description="Issue an infraction")
@app_commands.describe(
    user="User receiving infraction",
    punishment="Punishment",
    reason="Reason"
)
async def infract(interaction: discord.Interaction, user: discord.Member, punishment: str, reason: str):

    embed = discord.Embed(
        title="⚠️ Staff Infraction",
        description=(
            f"An infraction has been issued.\n\n"
            f"• **User:** {user.mention}\n"
            f"• **Punishment:** {punishment}\n"
            f"• **Reason:** {reason}"
        ),
        color=discord.Color.dark_red()
    )

    embed.set_footer(text=f"Issued By {interaction.user.display_name}")

    await interaction.response.send_message(
        content=user.mention,
        embed=embed
    )

bot.run(TOKEN)