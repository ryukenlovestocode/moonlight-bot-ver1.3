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

     @commands.command()
     async def fortune(self, ctx):
      fortunes = [
        "🌙 The moon says: trust the process.",
        "🌑 Darkness first. Growth later.",
        "✨ A win is closer than you think.",
        "🌕 Tonight is powerful for you.",
        "☄️ Chaos brings opportunity."
      ]

      await ctx.send(random.choice(fortunes))

    @commands.command()
    async def moonfact(self, ctx):
     facts = [
        "🌕 The Moon is drifting away from Earth by ~3.8 cm per year.",
        "🌑 There are moonquakes.",
        "🌓 The Moon has no atmosphere.",
        "🌙 Moonlight is reflected sunlight.",
        "☄️ Humans last visited the Moon in 1972."
     ]

     await ctx.send(random.choice(facts))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def roast(self, ctx, member: discord.Member):
     roasts = [
        "has main character energy… in the tutorial.",
        "is built different. Not better. Just different.",
        "survives purely on luck.",
        "thinks they’re mysterious. They’re just quiet.",
        "is lowkey powerful but doesn’t know it yet."
     ]

     await ctx.send(f"🔥 {member.mention} {random.choice(roasts)}")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cosmic(self, ctx):
     responses = [
        "🪐 Your aura is chaotic neutral.",
        "🌌 The universe is watching you closely.",
        "☄️ You’re overdue for a plot twist.",
        "🌑 Something big is brewing.",
        "✨ Luck is loading…"
     ]
     await ctx.send(random.choice(responses))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def luck(self, ctx):
     percent = random.randint(1, 100)

     if percent > 80:
         msg = "🍀 Insanely lucky today."
     elif percent > 50:
        msg = "✨ Decent luck. Play smart."
     elif percent > 30:
        msg = "🌑 Unstable energy."
     else:
        msg = "☄️ Avoid risky decisions."

     await ctx.send(f"{msg}\n**Luck Level:** `{percent}%`")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def comfort(self, ctx):
     messages = [
        "🌙 You’re doing better than you think.",
        "✨ Take a breath. You’re safe here.",
        "🌓 One step at a time.",
        "🌌 Even slow progress is progress.",
        "💜 Luna’s got your back."
     ]

     await ctx.send(random.choice(messages))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def prophecy(self, ctx):
     prophecies = [
        "A late night will change everything.",
        "You’ll win when you least expect it.",
        "Someone will surprise you soon.",
        "A decision is closer than it feels.",
        "Your patience will pay off."
     ]

     await ctx.send(f"🔮 **Prophecy:** {random.choice(prophecies)}")
    
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ship(self, ctx, user1: discord.Member = None, user2: discord.Member = None):
    
     if user1 is None:
        return await ctx.send("❌ Ship who? Mention at least one user.")

     if user2 is None:
        user2 = ctx.author

     if user1.id == user2.id:
        return await ctx.send("💀 You cannot ship someone with themselves.")

     percentage = random.randint(1, 100)

     if percentage >= 90:
        verdict = "💍 Soulmates detected."
        color = discord.Color.gold()
     elif percentage >= 70:
        verdict = "💖 Strong connection."
        color = discord.Color.pink()
     elif percentage >= 50:
        verdict = "💫 There’s something there."
        color = discord.Color.purple()
     elif percentage >= 30:
        verdict = "😬 It’s… complicated."
        color = discord.Color.orange()
     else:
        verdict = "💀 This ship sank."

     embed = discord.Embed(
        title="💞 Luna Ship Calculator",
        description=f"{user1.mention} ❤️ {user2.mention}",
        color=color
     )

     embed.add_field(
        name="💯 Compatibility",
        value=f"**{percentage}%**",
        inline=False
     )

     embed.add_field(
        name="🔮 Verdict",
        value=verdict,
        inline=False
    )

     embed.set_thumbnail(url=random.choice([
         user1.display_avatar.url,
        user2.display_avatar.url
     ]))

     embed.set_footer(text="MoonLight • Love is a risk 🌙")

     await ctx.send(embed=embed)

    

    
async def setup(bot):
    await bot.add_cog(Fun(bot))