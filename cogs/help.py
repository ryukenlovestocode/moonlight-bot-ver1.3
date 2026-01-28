import discord
from discord.ext import commands

class HelpMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx):
        pages = []

        # -------- PAGE 1 : GENERAL --------
        embed1 = discord.Embed(
            title="🌙 Luna Help — General",
            description="Navigate using ⬅️ ➡️ | ❌ to close",
            color=discord.Color.blurple()
        )
        embed1.add_field(
            name="📌 Basic Commands",
            value=(
                "`$ping` — Check bot status\n"
                "`$bal` — Check balance\n"
                "`$daily` — Claim daily reward\n"
                "`$leaderboard` — Top users"
            ),
            inline=False
        )
        embed1.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed1.set_footer(text="Page 1 / 4 • Made by Ryuken")
        pages.append(embed1)

        # -------- PAGE 2 : GAMBLING --------
        embed2 = discord.Embed(
            title="🎰 Gambling Commands",
            color=discord.Color.purple()
        )
        embed2.add_field(
            name="🎲 Casino",
            value=(
                "`$cf <amount> h/t` — Coinflip\n"
                "`$d <amount> <1> <2>` — Dice\n"
                "`$bj <amount>` — Blackjack\n"
                "`$fish <amount>` — Fishing\n"
                "`$sw <amount>` — Spin the wheel"
            ),
            inline=False
        )
        embed2.set_footer(text="Page 2 / 4 • Gamble responsibly 🌙")
        pages.append(embed2)

        # -------- PAGE 3 : MODERATION --------
        embed3 = discord.Embed(
            title="🛡️ Moderation Commands",
            color=discord.Color.red()
        )
        embed3.add_field(
            name="🔨 Staff Only",
            value=(
                "`$kick @user [reason]`\n"
                "`$ban @user [reason]`\n"
                "`$timeout @user <minutes>`\n"
                "`$warn @user [reason]`\n"
                "`$clear <amount | contains keyword | contains bots>`"
            ),
            inline=False
        )
        embed3.set_footer(text="Page 3 / 4 • Mods only")
        pages.append(embed3)

        # -------- PAGE 4 : FUN --------
        embed4 = discord.Embed(
            title="✨ Fun & Extras",
            color=discord.Color.green()
        )
        embed4.add_field(
            name="🎉 Fun Stuff",
            value=(
                "`$meow`\n"
                "`$ship @user`\n"
                "`$burncash <amount>`\n"
                "`$luna` — About the bot"
            ),
            inline=False
        )
        embed4.set_footer(text="Page 4 / 4 • Luna vibes 🌙")
        pages.append(embed4)

        # -------- SEND FIRST PAGE --------
        index = 0
        msg = await ctx.send(embed=pages[index])

        # Reactions
        await msg.add_reaction("⬅️")
        await msg.add_reaction("➡️")
        await msg.add_reaction("❌")

        def check(reaction, user):
            return (
                user == ctx.author
                and reaction.message.id == msg.id
                and str(reaction.emoji) in ["⬅️", "➡️", "❌"]
            )

        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add",
                    timeout=60,
                    check=check
                )

                if str(reaction.emoji) == "➡️":
                    index = (index + 1) % len(pages)
                    await msg.edit(embed=pages[index])

                elif str(reaction.emoji) == "⬅️":
                    index = (index - 1) % len(pages)
                    await msg.edit(embed=pages[index])

                elif str(reaction.emoji) == "❌":
                    await msg.delete()
                    break

                await msg.remove_reaction(reaction, user)

            except:
                # Timeout → silently stop
                break

async def setup(bot):
    await bot.add_cog(HelpMenu(bot))