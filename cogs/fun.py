import discord
from discord.ext import commands
import random
from datetime import datetime



class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot






    @commands.command()
    async def luna(self, ctx):
     embed = discord.Embed(
         title="🌙 Luna",
        description=(
            "I wasn’t born overnight.\n\n"
            "I was built line by line — through bugs, crashes, rage, "
            "and way too much caffeine.\n\n"
            "**I exist because someone refused to quit.**"
        ),
        color=discord.Color.purple()
     )

     embed.add_field(
         name="📜 Lines of Code",
        value="**3263+** lines",
        inline=False
     )

     embed.add_field(
        name="⏱️ Time Spent",
        value="~ **34 hours** of development",
        inline=False
     )

     embed.add_field(
        name="🧠 Built With",
        value="Patience, frustration, curiosity, and obsession",
        inline=False
     )

     embed.add_field(
        name="⭐️ Creator",
        value="**Ryuken**",
        inline=False
     )

     embed.set_thumbnail(url=self.bot.user.display_avatar.url)

     embed.set_footer(
        text="Moonlight • Made from chaos, polished with discipline"
     )

     await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))