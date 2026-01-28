import discord
from discord.ext import commands
import sqlite3
import random

DB_PATH = "database.db"

CLAN_CREATE_COST = 2_500_000
LEVEL_UP_AMOUNT = 10_000_000

ROLES = ["Member", "Elder", "General", "Co-Leader", "Leader"]

class Clans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------------- DB HELPERS ----------------
    def db(self):
        return sqlite3.connect(DB_PATH)

    def get_clan_of_user(self, user_id):
        con = self.db()
        cur = con.cursor()
        cur.execute("""
            SELECT clans.id, clans.name, clan_members.role
            FROM clan_members
            JOIN clans ON clans.id = clan_members.clan_id
            WHERE clan_members.user_id = ?
        """, (user_id,))
        data = cur.fetchone()
        con.close()
        return data

    # ---------------- CLAN CREATE ----------------
    @commands.command()
    async def clan(self, ctx, action: str, *args):

     if action.lower() == "create":
        if not args:
            return await ctx.send("❌ `$clan create <name>`")
        await self.create_clan(ctx, " ".join(args))

     elif action.lower() == "deposit":
        if not args:
            return await ctx.send("❌ `$clan deposit <amount>`")
        await self.deposit(ctx, args[0])

     elif action.lower() == "weekly":
        await self.weekly(ctx)

     elif action.lower() == "promote":
        if not ctx.message.mentions:
            return await ctx.send("❌ `$clan promote @user`")
        await self.promote(ctx, ctx.message.mentions[0])

     elif action.lower() == "invite":
        if not ctx.message.mentions:
            return await ctx.send("❌ `$clan invite @user`")
        await self.invite(ctx, ctx.message.mentions[0])

     elif action.lower() == "demote":
        if not ctx.message.mentions:
            return await ctx.send("❌ `$clan demote @user`")
        await self.demote(ctx, ctx.message.mentions[0])

    async def create_clan(self, ctx, name):
        if not name:
            return await ctx.send("❌ `$clan create <name>`")

        # balance check (replace with your economy function)
        from cogs.gambling import get_balance, remove_balance

        if get_balance(ctx.author.id) < CLAN_CREATE_COST:
            return await ctx.send("❌ You need **2.5M moonshards** to create a clan.")

        if self.get_clan_of_user(ctx.author.id):
            return await ctx.send("❌ You are already in a clan.")

        con = self.db()
        cur = con.cursor()

        try:
            cur.execute(
                "INSERT INTO clans (name, leader_id) VALUES (?, ?)",
                (name, ctx.author.id)
            )
            clan_id = cur.lastrowid

            cur.execute(
                "INSERT INTO clan_members VALUES (?, ?, ?)",
                (ctx.author.id, clan_id, "Leader")
            )

            remove_balance(ctx.author.id, CLAN_CREATE_COST)

            con.commit()
            await ctx.send(f"🏰 Clan **{name}** created successfully!")

        except sqlite3.IntegrityError:
            await ctx.send("❌ Clan name already exists.")

        con.close()

    # ---------------- DEPOSIT ----------------
    async def deposit(self, ctx, amount):
        if not amount or not amount.isdigit():
            return await ctx.send("❌ `$clan deposit <amount>`")

        amount = int(amount)

        from cogs.gambling import get_balance, remove_balance

        clan = self.get_clan_of_user(ctx.author.id)
        if not clan:
            return await ctx.send("❌ You are not in a clan.")

        if get_balance(ctx.author.id) < amount:
            return await ctx.send("❌ Insufficient balance.")

        con = self.db()
        cur = con.cursor()

        cur.execute(
            "UPDATE clans SET balance = balance + ? WHERE id = ?",
            (amount, clan[0])
        )

        cur.execute("SELECT balance, level FROM clans WHERE id = ?", (clan[0],))
        balance, level = cur.fetchone()

        if balance >= level * LEVEL_UP_AMOUNT:
            cur.execute(
                "UPDATE clans SET level = level + 1 WHERE id = ?",
                (clan[0],)
            )
            await ctx.send("🎉 **Clan leveled up!**")

        remove_balance(ctx.author.id, amount)
        con.commit()
        con.close()

        await ctx.send(f"💰 Deposited **{amount}** moonshards into the clan.")

    # ---------------- WEEKLY ----------------
    async def weekly(self, ctx):
        clan = self.get_clan_of_user(ctx.author.id)
        if not clan:
            return await ctx.send("❌ You are not in a clan.")

        reward = random.randint(150_000, 250_000)

        from cogs.gambling import add_balance
        add_balance(ctx.author.id, reward)

        await ctx.send(f"🎁 You received **{reward} moonshards** from clan weekly!")

    # ---------------- PROMOTE / DEMOTE ----------------
    async def promote(self, ctx, member: discord.Member):
        await self.change_role(ctx, member, up=True)

    async def demote(self, ctx, member: discord.Member):
        await self.change_role(ctx, member, up=False)

    async def change_role(self, ctx, member, up: bool):
        author_clan = self.get_clan_of_user(ctx.author.id)
        target_clan = self.get_clan_of_user(member.id)

        if not author_clan or not target_clan:
            return await ctx.send("❌ Clan mismatch.")

        if author_clan[0] != target_clan[0]:
            return await ctx.send("❌ Same clan only.")

        if author_clan[2] not in ["Leader", "Co-Leader"]:
            return await ctx.send("❌ Insufficient permissions.")

        current = target_clan[2]
        idx = ROLES.index(current)

        new_idx = idx + 1 if up else idx - 1
        if new_idx < 0 or new_idx >= len(ROLES):
            return await ctx.send("❌ Invalid role change.")

        new_role = ROLES[new_idx]

        con = self.db()
        cur = con.cursor()
        cur.execute(
            "UPDATE clan_members SET role = ? WHERE user_id = ?",
            (new_role, member.id)
        )
        con.commit()
        con.close()

        await ctx.send(f"🔰 **{member}** is now **{new_role}**.")

async def setup(bot):
    await bot.add_cog(Clans(bot))