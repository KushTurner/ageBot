import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import Paginator

load_dotenv()


intents = discord.Intents(members = True, guilds = True, message_content = True, messages=True)
bot = commands.Bot(command_prefix='-', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.command()
async def ageleaderboard(ctx, amount = 1):
    guild = bot.get_guild(ctx.guild.id)
    server_total = guild.member_count
    if amount > server_total:
        await ctx.send(f"Input amount less than {guild.member_count}")
        return
    if server_total == 2:
        amount = 2
    elif server_total == 1:
        amount = 1
    leaderboard = {}
    for member in guild.members:
        leaderboard[member.id] = member.created_at.date()
    leaderboard = sorted(leaderboard.items(), key=lambda item: item[1])
    
    messagelist = []
    temp = ''

    for i in range(amount):
        username = bot.get_user(leaderboard[i][0]).name
        joindate = bot.get_user(leaderboard[i][0]).created_at.strftime("%d/%m/%Y")
        temp = temp + ((f"\n{i+1}. {username} {joindate}"))
        if ((i+1) % 10 == 0):
            messagelist.append(temp)
            temp = ''
        elif (i+1 == amount):
            messagelist.append(temp)
            temp = ''

    embeds = []

    for i in range(len(messagelist)):
        embeds.append(discord.Embed(title="Leaderboard", description=messagelist[i]))

    PreviousButton = discord.ui.Button(label="<", style=discord.ButtonStyle.grey)
    NextButton = discord.ui.Button(label=">", style=discord.ButtonStyle.grey)
    InitialPage = 0 
    timeout = 60 

    await Paginator.Simple(
        PreviousButton=PreviousButton,
        NextButton=NextButton,
        InitialPage=InitialPage,
        timeout=timeout).start(ctx, pages=embeds)

bot.run(os.getenv('APIKEY'))
