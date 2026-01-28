import discord
from discord.ext import commands
from collections import defaultdict
from datetime import datetime, timedelta

# ---------------- CONFIG ----------------
STATS_WINDOW = timedelta(hours=24)

# { guild_id: [(user_id, timestamp), ...] }
message_stats = defaultdict(list)

# ---------------- COG ----------------
class Statistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ================= MESSAGE TRACKER =================
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        now = datetime.utcnow()
        guild_id = message.guild.id

        # Store message
        message_stats[guild_id].append((message.author.id, now))

        # Cleanup old messages
        cutoff = now - STATS_WINDOW
        message_stats[guild_id] = [
            (uid, ts) for uid, ts in message_stats[guild_id]
            if ts > cutoff
        ]

        # ⚠️ THIS MUST EXIST ONLY HERE
        await self.bot.process_commands(message)

    # ================= STATS COMMAND =================
    @commands.command(name="stats", aliases=["statistics"])
    @commands.has_permissions(manage_messages=True)
    async def stats(self, ctx, member: discord.Member = None):
        guild_id = ctx.guild.id
        now = datetime.utcnow()
        cutoff = now - STATS_WINDOW

        data = message_stats.get(guild_id, [])

        if not data:
            return await ctx.send("❌ No message data recorded yet.")

        # Count messages
        counts = defaultdict(int)
        hourly = defaultdict(lambda: defaultdict(int))

        for user_id, timestamp in data:
            if timestamp > cutoff:
                counts[user_id] += 1
                hourly[user_id][timestamp.hour] += 1

        # ================= USER STATS =================
        if member:
            total_messages = counts.get(member.id, 0)
            hours = hourly.get(member.id, {})

            if hours:
                peak_hour = max(hours, key=hours.get)
                peak_range = f"{peak_hour:02d}:00 – {peak_hour + 1:02d}:00 UTC"
                peak_count = hours[peak_hour]
            else:
                peak_range = "No data"
                peak_count = 0

            embed = discord.Embed(
                title="👤 User Message Statistics (24h)",
                color=discord.Color.purple()
            )

            embed.add_field(
                name="👤 User",
                value=member.mention,
                inline=False
            )

            embed.add_field(
                name="💬 Total Messages",
                value=f"**{total_messages}**",
                inline=False
            )

            embed.add_field(
                name="⏰ Most Active Time",
                value=f"**{peak_range}**\n({peak_count} messages)",
                inline=False
            )

            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text="MoonLight Statistics • Last 24 hours (UTC)")

            return await ctx.send(embed=embed)

        # ================= SERVER STATS =================
        total_messages = sum(counts.values())

        top_users = sorted(
            counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        leaderboard = ""
        for i, (user_id, count) in enumerate(top_users, start=1):
            member_obj = ctx.guild.get_member(user_id)
            name = member_obj.display_name if member_obj else f"User {user_id}"
            leaderboard += f"**{i}. {name}** — {count} messages\n"

        embed = discord.Embed(
            title="📊 Server Message Statistics (24h)",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="💬 Total Messages",
            value=f"**{total_messages}**",
            inline=False
        )

        embed.add_field(
            name="👥 Top Active Members",
            value=leaderboard or "No data",
            inline=False
        )

        embed.set_footer(text="MoonLight Statistics • Last 24 hours (UTC)")

        await ctx.send(embed=embed)

# ---------------- SETUP ----------------
async def setup(bot):
    await bot.add_cog(Statistics(bot))