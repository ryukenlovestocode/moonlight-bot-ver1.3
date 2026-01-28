import discord
from discord.ext import commands
from datetime import timedelta
from datetime import datetime
from collections import defaultdict

message_stats = defaultdict(list)

STATS_WINDOW = timedelta(hours=24)

# channel_id -> message data
sniped_messages = {}

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------------- KICK ----------------
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 **{member}** was kicked.\n📝 Reason: {reason}")

    # ---------------- BAN ----------------
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 **{member}** was banned.\n📝 Reason: {reason}")

    # ---------------- UNBAN ----------------
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"✅ **{user}** has been unbanned.")

    # ---------------- TIMEOUT ----------------
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, minutes: int, *, reason="No reason provided"):
        if minutes <= 0:
            return await ctx.send("❌ Timeout duration must be greater than 0 minutes.")

        duration = discord.utils.utcnow() + timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)

        await ctx.send(
            f"⏳ **{member}** has been muted for **{minutes} minutes**.\n"
            f"📝 Reason: {reason}"
        )

    # ---------------- CLEAR / PURGE ----------------
    @commands.command(name="clear", aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, *, arg: str):
        MAX_SCAN = 100        # how far back to look
        MAX_DELETE = 5       # max messages to delete

        # ---------------- BOT MESSAGES ----------------
        if arg.lower().startswith("contains bots"):
        # 🔥 DELETE THE COMMAND MESSAGE ITSELF
         await ctx.message.delete()

         deleted = []

         async for message in ctx.channel.history(limit=MAX_SCAN):
          if message.author.bot:
            deleted.append(message)
            if len(deleted) >= MAX_DELETE:
                break

         if not deleted:
          return await ctx.send(
            "🤖 No recent bot messages found.",
            delete_after=3
        )

         await ctx.channel.delete_messages(deleted)

         return await ctx.send(
        f"🤖 Deleted **{len(deleted)}** bot messages.",
        delete_after=3
    )

        # ---------------- KEYWORD ----------------
        if arg.lower().startswith("contains "):
            keyword = arg[9:].strip().lower()
            deleted = []

            if not keyword:
                return await ctx.send("❌ Please provide a keyword.")

            async for message in ctx.channel.history(limit=MAX_SCAN):
                if keyword in message.content.lower():
                    deleted.append(message)
                    if len(deleted) >= MAX_DELETE:
                        break

            if not deleted:
                return await ctx.send(
                    f"🔍 No recent messages found containing **'{keyword}'**.",
                    delete_after=3
                )

            await ctx.channel.delete_messages(deleted)
            return await ctx.send(
                f"🔍 Deleted **{len(deleted)}** messages containing **'{keyword}'**.",
                delete_after=3
            )

        # ---------------- NUMBER ----------------
        try:
            amount = int(arg)
        except ValueError:
            return await ctx.send(
                "❌ Invalid usage.\n"
                "Use:\n"
                "`$clear <amount>`\n"
                "`$clear contains <keyword>`\n"
                "`$clear contains bots`"
            )

        if amount <= 0:
            return await ctx.send("❌ Enter a valid number of messages.")

        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(
            f"🧹 Deleted **{len(deleted) - 1}** messages.",
            delete_after=3
        )
    # ---------------- WARN ----------------
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await ctx.send(
            f"⚠️ **{member.mention}** has been warned.\n📝 Reason: {reason}"
        )

    #----------------SNIPE------------------
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        sniped_messages[message.channel.id] = {
            "author": message.author,
            "content": message.content if message.content else "*[No text]*",
            "time": datetime.utcnow(),
            "avatar": message.author.display_avatar.url
        }

    @commands.command(name="s", aliases=["snipe"])
    @commands.has_permissions(manage_messages=True)
    async def snipe(self, ctx):
        data = sniped_messages.get(ctx.channel.id)

        if not data:
            return await ctx.send("❌ Nothing to snipe here.")

        embed = discord.Embed(
            title="🎯 Sniped Message",
            description=data["content"],
            color=discord.Color.dark_purple(),
            timestamp=data["time"]
        )

        embed.set_author(
            name=str(data["author"]),
            icon_url=data["avatar"]
        )

        embed.set_footer(text="MoonLight Moderation • Deleted message")

        await ctx.send(embed=embed)
    @commands.Cog.listener()
    async def on_message(self, message):
     if message.author.bot or not message.guild:
        return

     now = datetime.utcnow()
     guild_id = message.guild.id

     # Add message
     message_stats[guild_id].append((message.author.id, now))

     # Cleanup old messages
     cutoff = now - STATS_WINDOW
     message_stats[guild_id] = [
        (uid, ts) for uid, ts in message_stats[guild_id]
        if ts > cutoff
     ]

     


# ---------------- STATS -----------------
    @commands.command(name="stats", aliases=["statistics"])
    @commands.has_permissions(manage_messages=True)
    async def stats(self, ctx, member: discord.Member = None):
     guild_id = ctx.guild.id
     now = datetime.utcnow()
     cutoff = now - STATS_WINDOW
 
     data = message_stats.get(guild_id, [])

     if not data:
        return await ctx.send("❌ No message data recorded yet.")

     # Count messages per user + per hour
     counts = defaultdict(int)
     hourly_counts = defaultdict(lambda: defaultdict(int))

     for user_id, timestamp in data:
        if timestamp > cutoff:
            counts[user_id] += 1
            hourly_counts[user_id][timestamp.hour] += 1

    # ---------------- USER STATS ----------------
     if member:
        total_messages = counts.get(member.id, 0)
        user_hours = hourly_counts.get(member.id, {})

        if user_hours:
            peak_hour = max(user_hours, key=user_hours.get)
            peak_count = user_hours[peak_hour]
            peak_time = f"{peak_hour:02d}:00 – {peak_hour + 1:02d}:00 UTC"
        else:
            peak_time = "No data"
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
            value=f"**{total_messages}** messages",
            inline=False
        )

        embed.add_field(
            name="⏰ Most Active Time",
            value=f"**{peak_time}**\n({peak_count} messages)",
            inline=False
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="MoonLight Moderation • Last 24 hours (UTC)")

        return await ctx.send(embed=embed)

    # ---------------- SERVER STATS ----------------
     total_messages = sum(counts.values())

     top_users = sorted(
        counts.items(),
        key=lambda x: x[1],
        reverse=True
     )[:10]

     embed = discord.Embed(
        title="📊 Server Message Statistics (24h)",
        color=discord.Color.blurple()
     )

     embed.add_field(
        name="💬 Total Messages",
        value=f"**{total_messages}** messages",
        inline=False
     )

     leaderboard = ""
     for i, (user_id, count) in enumerate(top_users, start=1):
        member_obj = ctx.guild.get_member(user_id)
        name = member_obj.display_name if member_obj else f"User {user_id}"
        leaderboard += f"**{i}. {name}** — {count} messages\n"

     embed.add_field(
        name="👥 Top Active Members",
        value=leaderboard or "No data",
        inline=False
     )

     embed.set_footer(text="MoonLight Moderation • Last 24 hours (UTC)")

     await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))