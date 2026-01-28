import discord
import os
from discord.ext import commands
import subprocess

try:
    subprocess.run(["ffmpeg", "-version"], check=True)
    print("✅ FFMPEG FOUND")
except Exception as e:
    print("❌ FFMPEG NOT FOUND:", e)

# ---------- INTENTS ----------
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.voice_states = True

# ---------- BOT ----------
bot = commands.Bot(
    command_prefix="$",
    intents=intents,
    help_command=None  # 🔥 disables default help
)

# ---------- GLOBAL ERROR HANDLER ----------
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send("❌ **You're not a moderator, dumbo.**")

    if isinstance(error, commands.BotMissingPermissions):
        return await ctx.send("⚠️ I don’t have the required permissions to do that.")

    if isinstance(error, commands.CommandOnCooldown):
        return await ctx.send(
            f"⏳ Chill! Try again in **{error.retry_after:.1f}s**."
        )

    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send("❌ Missing required arguments.")

    if isinstance(error, commands.BadArgument):
        return await ctx.send("❌ Invalid argument provided.")

    if isinstance(error, commands.CommandNotFound):
        return  # ignore silently

    raise error  # raise unexpected errors for debugging

# ---------- READY ----------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# ---------- LOAD COGS ----------
@bot.event
async def setup_hook():
    await bot.load_extension("cogs.utility")
    await bot.load_extension("cogs.gambling")
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.welcomer")
    await bot.load_extension("cogs.help")
    await bot.load_extension("cogs.music")
    print("✅ Cogs loaded")

# ---------- RUN ----------
bot.run(os.getenv("DISCORD_TOKEN"))