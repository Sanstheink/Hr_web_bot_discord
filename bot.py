import discord
from discord.ext import commands
import requests
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

HR_API_URL = "https://your-render-hr-web.onrender.com/api/push"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def checkin(ctx):
    payload = {
        "user_id": str(ctx.author.id),
        "name": ctx.author.name,
        "action": "checkin",
        "timestamp": datetime.utcnow().isoformat()
    }
    requests.post(HR_API_URL, json=payload)
    await ctx.send(f"{ctx.author.mention} เข้างานเรียบร้อยแล้ว!")

@bot.command()
async def checkout(ctx):
    payload = {
        "user_id": str(ctx.author.id),
        "name": ctx.author.name,
        "action": "checkout",
        "timestamp": datetime.utcnow().isoformat()
    }
    requests.post(HR_API_URL, json=payload)
    await ctx.send(f"{ctx.author.mention} ออกงานเรียบร้อยแล้ว!")

bot.run("YOUR_DISCORD_BOT_TOKEN")
