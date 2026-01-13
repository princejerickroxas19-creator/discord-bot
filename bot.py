import discord
from discord import app_commands
import asyncio

# ============================================
# PASTE YOUR BOT TOKEN HERE
# ============================================
TOKEN = "MTQ2MDQ1Nzc1MzAyODg1ODAyMA.GLnDV-.YFlyPQuRj9X9UUnN6bLmBFfNCzi5J1RuMwFRdE"

# ============================================
# PASTE YOUR SERVER ID HERE (for instant updates)
# ============================================
GUILD_ID = None  # Replace with your server ID number, e.g., 1234567890

# ============================================
# BOT SETUP
# ============================================
class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self):
        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print(f"✅ Commands synced to server {GUILD_ID} (INSTANT)")
        else:
            await self.tree.sync()
            print("✅ Commands synced globally (takes 1-2 minutes)")

bot = MyBot()

# ============================================
# WHEN BOT IS READY
# ============================================
@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    print(f"✅ Bot ID: {bot.user.id}")
    print("✅ Ready to receive commands!")
    print("=" * 50)

# ============================================
# /result COMMAND
# ============================================
@bot.tree.command(name="result", description="Post PvP test results")
async def result(
    interaction: discord.Interaction,
    testee: discord.Member,
    tester: discord.Member,
    gamemodes: str,
    scores: str,
    winner: str,
    status: str
):
    print(f"Command received from {interaction.user}")
    
    # Respond immediately
    await interaction.response.defer()
    
    try:
        # Parse gamemodes and scores
        gamemode_list = [g.strip() for g in gamemodes.split(",") if g.strip()]
        score_list = [s.strip() for s in scores.split(",") if s.strip()]
        
        # Build gamemode results text
        gamemode_text = ""
        for i, gamemode in enumerate(gamemode_list):
            if i < len(score_list):
                score = score_list[i]
                gamemode_text += f"**{gamemode.upper()}** ( {score} )\n"
            else:
                gamemode_text += f"**{gamemode.upper()}** ( N/A )\n"
        
        # Determine embed color based on status
        if status.upper() in ["ACCEPTED", "PASSED"]:
            color = discord.Color.green()
        elif status.upper() in ["DECLINED", "FAILED"]:
            color = discord.Color.red()
        else:
            color = discord.Color.blue()
        
        # Create embed
        embed = discord.Embed(
            title="PvP Test Results",
            color=color,
            timestamp=interaction.created_at
        )
        
        embed.add_field(name="Testee", value=testee.mention, inline=True)
        embed.add_field(name="Tester", value=tester.mention, inline=True)
        embed.add_field(name="\u200b", value="", inline=False)  # Blank line
        
        embed.add_field(name="Gamemodes & Scores", value=gamemode_text or "No gamemodes", inline=False)
        
        embed.add_field(name="Winner", value=f"**{winner.upper()}**", inline=True)
        embed.add_field(name="Status", value=f"**{status.upper()}**", inline=True)
        
        embed.set_footer(text=f"Recorded by {interaction.user.display_name}")
        
        # Send response
        await interaction.followup.send(embed=embed)
        print("✅ Response sent successfully")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        try:
            await interaction.followup.send(f"Error: {str(e)}", ephemeral=True)
        except:
            pass

# ============================================
# RUN BOT
# ============================================
print("=" * 50)
print("Starting bot...")
print("=" * 50)

if TOKEN == "YOUR_BOT_TOKEN_HERE":
    print("❌ ERROR: You need to set your bot token!")
    print("❌ Open bot.py and replace YOUR_BOT_TOKEN_HERE with your actual token")
    input("Press Enter to exit...")
else:
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ ERROR: Invalid bot token!")
        print("❌ Make sure you copied the token correctly")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        input("Press Enter to exit...")