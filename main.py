import os
import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread

TOKEN = os.getenv("DISCORD_TOKEN")

ALLOWED_ROLE = "DB | Leadership"
DEPLOYMENT_PING_ROLE = "NCIS | Agent"

PROMOTION_IMAGE = "https://cdn.discordapp.com/attachments/1469039919338098731/1513627752442499122/content.png?ex=6a286b32&is=6a2719b2&hm=5196198053e868cd7c81f6111090ffc061dd22af1d584966c68451ed90376c6d&"
INFRACTION_IMAGE = "https://cdn.discordapp.com/attachments/1469039919338098731/1513628298012266626/content.png?ex=6a286bb4&is=6a271a34&hm=c1ff65bf4f952f63d01425d38f77080a502987c7d6513ff20fe3a0d2e9236488&"
DEPLOYMENT_IMAGE = "https://cdn.discordapp.com/attachments/1469039919338098731/1513630463795663001/content.png?ex=6a286db8&is=6a271c38&hm=e0ffeff004f82039c1d9a1f01dd5a025b9667886139d6c9401f995e8ff870660&"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running."

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


def is_leadership(interaction: discord.Interaction):
    return any(role.name == ALLOWED_ROLE for role in interaction.user.roles)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


@bot.tree.command(name="promote", description="Promote a member")
@app_commands.check(is_leadership)
async def promote(interaction: discord.Interaction, user: discord.Member, rank: discord.Role, reason: str):
    await interaction.response.defer()

    try:
        await user.add_roles(rank)

        embed = discord.Embed(
            title="Promotion Issue",
            description=(
                "*A promotion has been issued after careful discussion among High Ranking members of the bureau.*\n\n"
                f"• **User:** {user.mention}\n\n"
                f"• **New Rank:** {rank.mention}\n\n"
                f"• **Reason:** {reason}\n\n"
                f"***Issued by:*** {interaction.user.mention}\n\n"
                "Remember,\n"
                "***\"With great power, comes great responsibility.\"***"
            ),
            color=discord.Color.green()
        )

        embed.set_image(url=PROMOTION_IMAGE)
        embed.set_footer(text="NYPD | DB Utilities")

        await interaction.followup.send(content=user.mention, embed=embed)

    except discord.Forbidden:
        await interaction.followup.send(
            "❌ I cannot give that role. Move my bot role above that role and give me Manage Roles.",
            ephemeral=True
        )


@bot.tree.command(name="infract", description="Issue an infraction")
@app_commands.check(is_leadership)
async def infract(interaction: discord.Interaction, user: discord.Member, type: discord.Role, reason: str):
    await interaction.response.defer()

    try:
        await user.add_roles(type)

        embed = discord.Embed(
            title="Infraction Issue",
            description=(
                "*An infraction has been issued after careful review by DB Leadership.*\n\n"
                f"• **User:** {user.mention}\n\n"
                f"• **Type:** {type.mention}\n\n"
                f"• **Reason:** {reason}\n\n"
                f"***Issued by:*** {interaction.user.mention}"
            ),
            color=discord.Color.red()
        )

        embed.set_image(url=INFRACTION_IMAGE)
        embed.set_footer(text="NYPD | DB Utilities")

        await interaction.followup.send(content=user.mention, embed=embed)

    except discord.Forbidden:
        await interaction.followup.send(
            "❌ I cannot give that infraction role. Move my bot role above that role and give me Manage Roles.",
            ephemeral=True
        )


@bot.tree.command(name="deployment", description="Issue an NCIS deployment")
@app_commands.check(is_leadership)
async def deployment(interaction: discord.Interaction, location: str, starting_time: str, notes: str):
    await interaction.response.defer()

    ping_role = discord.utils.get(interaction.guild.roles, name=DEPLOYMENT_PING_ROLE)

    embed = discord.Embed(
        title="NCIS Deployment - Active Operation",
        description=(
            "====================================\n"
            "The **Naval Criminal Investigative Service** is hosting an official deployment. "
            "All available NCIS agents are ordered to report, clock in, and remain active.\n"
            "====================================\n\n"
            "**Deployment Information**\n\n"
            f"Host: {interaction.user.mention}\n"
            "Division: Naval Criminal Investigative Service\n"
            "Operation Type: Field Deployment\n"
            f"Location: {location}\n"
            f"Starting Time: {starting_time}\n"
            f"Notes: {notes}\n\n"
            "====================================\n\n"
            "**Rules:**\n\n"
            "• Turn your shifts on.\n"
            "• Follow all orders from NCIS Command.\n"
            "• Remain professional and disciplined.\n"
            "• Patrol within assigned jurisdiction.\n"
            "• Do not leave post without permission.\n"
            "• Maintain radio communication at all times.\n\n"
            "**NCIS | Naval Criminal Investigative Service**"
        ),
        color=discord.Color.teal()
    )

    embed.set_image(url=DEPLOYMENT_IMAGE)
    embed.set_footer(text="NYPD | DB Utilities")

    await interaction.followup.send(
        content=ping_role.mention if ping_role else "",
        embed=embed
    )


@promote.error
@infract.error
@deployment.error
async def permission_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CheckFailure):
        if interaction.response.is_done():
            await interaction.followup.send("❌ You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)


if TOKEN is None:
    raise ValueError("DISCORD_TOKEN is missing in Render Environment Variables.")

Thread(target=run_web).start()
bot.run(TOKEN)