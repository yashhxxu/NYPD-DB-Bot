import os
import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread

TOKEN = os.getenv("DISCORD_TOKEN")

LEADERSHIP_ROLES = ["DB | Leadership", "DB | Supervisor"]
AGENT_ROLE = "NCIS | Agent"
DEPLOYMENT_PING_ROLE = "NCIS | Agent"

PROMOTION_IMAGE = "https://cdn.discordapp.com/attachments/1469039919338098731/1513627752442499122/content.png?ex=6a286b32&is=6a2719b2&hm=5196198053e868cd7c81f6111090ffc061dd22af1d584966c68451ed90376c6d&"
INFRACTION_IMAGE = "https://cdn.discordapp.com/attachments/1469039919338098731/1513628298012266626/content.png?ex=6a286bb4&is=6a271a34&hm=c1ff65bf4f952f63d01425d38f77080a502987c7d6513ff20fe3a0d2e9236488&"
DEPLOYMENT_IMAGE = "https://cdn.discordapp.com/attachments/1469039919338098731/1513630463795663001/content.png?ex=6a286db8&is=6a271c38&hm=e0ffeff004f82039c1d9a1f01dd5a025b9667886139d6c9401f995e8ff870660&"
INCIDENT_IMAGE = "https://cdn.discordapp.com/attachments/1469039919338098731/1513790083663396864/content.png?ex=6a290260&is=6a27b0e0&hm=fdf057c0eafe0db59a7f77e8ac7cb0e0fffce43d5065f54b61b231c412ba1216&"
ARREST_IMAGE = "https://cdn.discordapp.com/attachments/1469039919338098731/1513792105301016626/content.png?ex=6a290442&is=6a27b2c2&hm=cfeda7f5840a8c5870a635fa6560b980f0a14c8db53842e254588fbfc15355fc&"

app = Flask(__name__)

@app.route("/")
def home():
    return "NYPD | DB Bot is running."

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def has_role(interaction: discord.Interaction, role_name: str):
    return any(role.name == role_name for role in interaction.user.roles)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

    print(f"Logged in as {bot.user}")

def is_agent(interaction: discord.Interaction):
    return has_role(interaction, AGENT_ROLE)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="promote", description="Promote a member")
@app_commands.check(is_leadership)
async def promote(
    interaction: discord.Interaction,
    user: discord.Member,
    rank: discord.Role,
    reason: str,
    notes: str = "No notes provided."
):
    await interaction.response.defer()

    try:
        await user.add_roles(rank, reason=f"Promotion issued by {interaction.user}")

        embed = discord.Embed(
            title="Promotion Issue",
            description=(
                "*A promotion has been issued after careful discussion among High Ranking members of the bureau.*\n\n"
                f"• **User:** {user.mention}\n\n"
                f"• **New Rank:** {rank.mention}\n\n"
                f"• **Reason:** {reason}\n\n"
                f"• **Notes:** {notes}\n\n"
                f"***Issued by:*** {interaction.user.mention}\n\n"
                "Remember,\n"
                "***\"With great power, comes great responsibility.\"***"
            ),
            color=discord.Color.green()
        )

        embed.set_image(url=PROMOTION_IMAGE)
        embed.set_footer(text="NYPD | DB Utilities")

        await interaction.followup.send(content=user.mention, embed=embed)

    except Exception as e:
        await interaction.followup.send(
            f"❌ Error while running promotion command:\n```{e}```",
            ephemeral=True
        )

@bot.tree.command(name="infract", description="Issue an infraction")
@app_commands.check(is_leadership)
async def infract(
    interaction: discord.Interaction,
    user: discord.Member,
    infraction_type: discord.Role,
    reason: str,
    notes: str = "No notes provided."
):
    await interaction.response.defer()

    try:
        await user.add_roles(infraction_type, reason=f"Infraction issued by {interaction.user}")

        embed = discord.Embed(
            title="Infraction Issue",
            description=(
                "*An infraction has been issued after careful review by DB Leadership.*\n\n"
                f"• **User:** {user.mention}\n\n"
                f"• **Type:** {infraction_type.mention}\n\n"
                f"• **Reason:** {reason}\n\n"
                f"• **Notes:** {notes}\n\n"
                f"***Issued by:*** {interaction.user.mention}"
            ),
            color=discord.Color.red()
        )

        embed.set_image(url=INFRACTION_IMAGE)
        embed.set_footer(text="NYPD | DB Utilities")

        await interaction.followup.send(content=user.mention, embed=embed)

    except Exception as e:
        await interaction.followup.send(
            f"❌ Error while running infraction command:\n```{e}```",
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

@bot.tree.command(name="incidentlog", description="Create an NCIS incident log")
@app_commands.check(is_agent)
async def incidentlog(
    interaction: discord.Interaction,
    agent_name: str,
    location: str,
    report: str,
    marker1: str = None,
    marker2: str = None,
    marker3: str = None,
    marker4: str = None,
    marker5: str = None,
    marker6: str = None,
    marker7: str = None,
    marker8: str = None,
    marker9: str = None,
    marker10: str = None,
    marker11: str = None
):
    await interaction.response.defer()

    markers = [marker1, marker2, marker3, marker4, marker5, marker6, marker7, marker8, marker9, marker10, marker11]
    marker_text = ""

    for index, marker in enumerate(markers, start=1):
        if marker:
            marker_text += f"• **Marker {index}:** {marker}\n"

    if marker_text == "":
        marker_text = "No markers were submitted."

    embed = discord.Embed(
        title="NCIS Incident Log",
        description=(
            "*An official NCIS incident report has been filed for bureau records. "
            "All submitted information is to be treated as operational documentation.*\n\n"
            f"• **Agent Name:** {agent_name}\n\n"
            f"• **Location:** {location}\n\n"
            f"• **Report:** {report}\n\n"
            "**Markers:**\n"
            f"{marker_text}\n"
            f"***Filed by:*** {interaction.user.mention}"
        ),
        color=discord.Color.dark_blue()
    )

    embed.set_image(url=INCIDENT_IMAGE)
    embed.set_footer(text="NCIS | Incident Documentation")

    await interaction.followup.send(embed=embed)

@bot.tree.command(name="arrestlog", description="Create an NCIS arrest log")
@app_commands.check(is_agent)
async def arrestlog(
    interaction: discord.Interaction,
    arresting_agent: str,
    assisting_agent: str,
    suspect_name: str,
    crime_committed: str,
    mugshot: discord.Attachment = None
):
    await interaction.response.defer()

    embed = discord.Embed(
        title="NCIS Arrest Log",
        description=(
            "*An arrest has been documented under NCIS authority. "
            "This record confirms the suspect, charges, and agents involved in the apprehension.*\n\n"
            f"• **Arresting Agent:** {arresting_agent}\n\n"
            f"• **Assisting Agent:** {assisting_agent}\n\n"
            f"• **Suspect's Name:** {suspect_name}\n\n"
            f"• **Crime Committed:** {crime_committed}\n\n"
            f"***Filed by:*** {interaction.user.mention}"
        ),
        color=discord.Color.orange()
    )

    if mugshot:
        embed.set_image(url=mugshot.url)
        embed.set_thumbnail(url=ARREST_IMAGE)
    else:
        embed.set_image(url=ARREST_IMAGE)

    embed.set_footer(text="NCIS | Arrest Documentation")

    await interaction.followup.send(embed=embed)

@promote.error
@infract.error
@deployment.error
@incidentlog.error
@arrestlog.error
async def command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CheckFailure):
        message = "❌ You do not have permission to use this command."
    else:
        message = f"❌ Command error:\n```{error}```"

    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)

if TOKEN is None:
    raise ValueError("DISCORD_TOKEN is missing in Render Environment Variables.")

web_thread = Thread(target=run_web)
web_thread.daemon = True
web_thread.start()

bot.run(TOKEN)