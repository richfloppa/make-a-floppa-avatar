import discord
from discord.ext import commands, tasks
import aiohttp
import asyncio
import os
from keep_alive import keep_alive
keep_alive()

intents = discord.Intents.all()
intents.typing = False
intents.presences = True

bot = commands.Bot(command_prefix='&', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    change_avatar.start()

@bot.event
async def on_message(message):
    if "floppa" in message.content.lower():
        await bot.user.edit(avatar=await download_avatar("https://media.discordapp.net/attachments/1121779036360806433/1170673973990805594/Screenshot_20231105_134014.jpg?ex=6559e619&is=65477119&hm=dbda749bd20e434a56f71be6"))
        await asyncio.sleep(10)  # Wait for 50 seconds
        await bot.user.edit(avatar=await download_avatar("https://media.discordapp.net/attachments/1192390233170382959/1194966157615169608/78e65b83-86d2-45dc-98fc-284d0f7cb5f0.jpg?ex=65b245f5&is=659fd0f5&hm=0d996a587514def4f285a2080dd4692bc9b206ad2ff7af157383300b54375fb9&"))

async def download_avatar(avatar_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(avatar_url) as response:
            if response.status == 200:
                avatar_bytes = await response.read()
                return avatar_bytes

@tasks.loop(minutes=10)
async def change_avatar():
    avatar_url = "https://media.discordapp.net/attachments/1192390233170382959/1194966157615169608/78e65b83-86d2-45dc-98fc-284d0f7cb5f0.jpg?ex=65b245f5&is=659fd0f5&hm=0d996a587514def4f285a2080dd4692bc9b206ad2ff7af157383300b54375fb9&"
    await bot.user.edit(avatar=await download_avatar(avatar_url))

@bot.event
async def on_disconnect():
    print("Bot disconnected. Reconnecting...")

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Error in {event}: {args[0]}")
    if isinstance(args[0], discord.ConnectionClosed):
        print("Reconnecting...")
        await asyncio.sleep(5)  # Add a delay before attempting to reconnect
        await bot.login(token, bot=True)
        await bot.connect()

token = os.getenv("token")

if token is None:
    print("Error: Token not found in environment variables.")
else:
    bot.run(token)
