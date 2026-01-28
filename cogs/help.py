import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="📖 Luna Help Menu",
            description="Here’s what I can help you with 🌙",
            color=discord.Color.blurple()
        )

        # 🖼️ Luna bot profile picture
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        # 🎲 Gambling / Economy
        embed.add_field(
            name="🎲 Economy & Games",
            value=(
                "`$bal` – Check your balance\n"
                "`$daily` – Claim daily reward\n"
                "`$cf <amount> h/t` – Coinflip\n"
                "`$d <amount> <1> <2>` – Dice roll\n"
                "`$bj <amount>` – Blackjack\n"
                "`$lb` – Leaderboard"
                "'$fish <amount>' – Fishing\n"
            ),
            inline=False
        )

        # 🛠️ Moderation
        embed.add_field(
            name="🛠️ Moderation",
            value=(
                "`$kick @user [reason]`\n"
                "`$ban @user [reason]`\n"
                "`$unban <user_id>`\n"
                "`$timeout @user <minutes> [reason]`\n"
                "`$clear <amount>`\n"
                "`$clear contains <keyword|bots>`"
            ),
            inline=False
        )

        # 🧰 Utility
        embed.add_field(
            name="🧰 Utility",
            value=(
                "`$afk <reason>`\n"
                "`$av @user` – View avatar\n"
                "`$help` – Show this menu"
            ),
            inline=False
        )

        embed.set_footer(
            text="🌙 MoonLight | Made by Ryuken"
        )

        await ctx.send(embed=embed)
        

async def setup(bot):
    await bot.add_cog(Help(bot))