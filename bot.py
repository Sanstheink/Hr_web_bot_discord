import discord
from discord.ext import commands
import requests
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

HR_API_URL = "https://honglub-discord-hr.onrender.com"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

def get_user_status(user_id):
    try:
        response = requests.get(f"{HR_API_URL}/status/{user_id}")
        if response.status_code == 200:
            return response.json().get("status", "active")
        else:
            return "active"
    except:
        return "active"

@bot.command()
async def checkin(ctx):
    user_id = str(ctx.author.id)
    if get_user_status(user_id) == "revoked":
        await ctx.send(f"{ctx.author.mention} คุณถูกเพิกถอนสิทธิ์การใช้งานบอทชั่วคราว")
        return

    payload = {
        "user_id": user_id,
        "name": ctx.author.name,
        "action": "checkin",
        "timestamp": datetime.utcnow().isoformat()
    }
    requests.post(HR_API_URL, json=payload)
    await ctx.send(f"{ctx.author.mention} เข้างานเรียบร้อยแล้ว!")

@bot.command()
async def checkout(ctx):
    user_id = str(ctx.author.id)
    if get_user_status(user_id) == "revoked":
        await ctx.send(f"{ctx.author.mention} คุณถูกเพิกถอนสิทธิ์การใช้งานบอทชั่วคราว")
        return

    payload = {
        "user_id": user_id,
        "name": ctx.author.name,
        "action": "checkout",
        "timestamp": datetime.utcnow().isoformat()
    }
    requests.post(HR_API_URL, json=payload)
    await ctx.send(f"{ctx.author.mention} ออกงานเรียบร้อยแล้ว!")

@bot.command()
@commands.has_permissions(administrator=True)
async def revoke(ctx, member: discord.Member):
    payload = {
        "user_id": str(member.id),
        "action": "revoke"
    }
    response = requests.post(f"{HR_API_URL}/permission", json=payload)
    if response.status_code == 200:
        await ctx.send(f"{member.mention} ถูกเพิกถอนสิทธิ์ใช้งานบอทชั่วคราวแล้ว")
    else:
        await ctx.send("เกิดข้อผิดพลาดในการเพิกถอนสิทธิ์")

@bot.command()
@commands.has_permissions(administrator=True)
async def restore(ctx, member: discord.Member):
    payload = {
        "user_id": str(member.id),
        "action": "restore"
    }
    response = requests.post(f"{HR_API_URL}/permission", json=payload)
    if response.status_code == 200:
        await ctx.send(f"{member.mention} ได้รับสิทธิ์ใช้งานบอทคืนแล้ว")
    else:
        await ctx.send("เกิดข้อผิดพลาดในการคืนสิทธิ์")

bot.run("MTM3NTYzMTI1ODg1OTYwMTk4MA.G78ZIw.pBeA0Ei84AzGkYjxhsvuupy9l3yJRwuPNjpGcQ")
