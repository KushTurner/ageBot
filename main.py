import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()



intents = discord.Intents(members = True, guilds = True, message_content = True, messages=True)
bot = commands.Bot(command_prefix='-', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.command()
async def ageboard(ctx, amount = 3):
    guild = bot.get_guild(ctx.guild.id)
    server_total = guild.member_count
    if server_total == 2:
        amount = 2
    elif server_total == 1:
        amount = 1
    if amount > server_total:
        await ctx.send(f"Input amount less than {guild.member_count}")
        return

    leaderboard = {}
    for member in guild.members:
        leaderboard[member.id] = member.created_at.date()
    leaderboard = sorted(leaderboard.items(), key=lambda item: item[1])
    
    message = str()

    for i in range(amount):
        username = bot.get_user(leaderboard[i][0]).name
        joindate = bot.get_user(leaderboard[i][0]).created_at.strftime("%d/%m/%Y")
        message = message + (f"\n{i+1}. {username} {joindate}")
    await ctx.send(message)
    
    


        

bot.run(os.getenv('APIKEY'))
