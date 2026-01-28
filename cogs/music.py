import discord
from discord.ext import commands
import yt_dlp
import asyncio

YDL_OPTIONS = {
    "format": "bestaudio/best",
    "quiet": True,
    "noplaylist": True
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("❌ You’re not in a voice channel.")

        await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("❌ I’m not in a voice channel.")

    @commands.command()
    async def play(self, ctx, *, query: str):
        if ctx.author.voice is None:
            return await ctx.send("❌ Join a voice channel first.")

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()

        vc = ctx.voice_client

        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(query, download=False)
            url = info["url"]
            title = info.get("title", "Unknown")

        source = await discord.FFmpegOpusAudio.from_probe(
            url, **FFMPEG_OPTIONS
        )

        vc.stop()
        vc.play(source)

        await ctx.send(f"🎶 **Now Playing:** {title}")

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Paused.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Resumed.")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.send("⏹️ Stopped.")

async def setup(bot):
    await bot.add_cog(Music(bot))