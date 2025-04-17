import os
import json
import sys
import discord
import src.polaroid_pack.poloriod_check as polaroid_check
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks
from src.noi_pack.noi_livekeeper import awake
from src.noi_pack.noi_command import register_commands
from src.trading_pack.commodity_management import register_commodity_image_commands
from src.polaroid_pack.poloriod_check import register_polaroid_check_commands


@tasks.loop(minutes=0.1)
async def check_stock_loop():
    try:
        with open('previous_stock.json', 'r') as f:
            previous_stock = json.load(f)
    except FileNotFoundError:
        previous_stock = []
   
    current_stock = await polaroid_check.fetch_stock_data()

    for item in current_stock:
        if item['style'] in ['瑟琳款', '可可莉克款']:
         
            prev_item = next((x for x in previous_stock if x['style'] == item['style']), None)
          
            if prev_item and not prev_item['in_stock'] and item['in_stock']:
                channel = bot.get_channel(1361897041009184768) 
                await channel.send(f"<@zero._an > {item['style']}有貨了") 
    
    
    with open('previous_stock.json', 'w') as f:
        json.dump(current_stock, f)

intents = discord.Intents.default()
intents.message_content = True  
intents.members = True

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')
load_dotenv(env_path)

noi_token = os.getenv('noi_token')

bot = commands.Bot(command_prefix='$', intents=intents)

register_commands(bot)
register_commodity_image_commands(bot)
register_polaroid_check_commands(bot)

async def sync_command_logic(bot):
    await bot.tree.sync()
    print("synced") 
    return

@bot.command()
async def synccommand(ctx):
    await ctx.message.delete()
    await sync_command_logic(bot)
    await ctx.send("synced")
    print(f'Synced by {ctx.author}...')

@bot.command()
async def restart(ctx):
    await ctx.message.delete()
    await ctx.send("restarting...")
    print(f'Restarting by {ctx.author}...')
    os.execv(sys.executable, [sys.executable, os.path.abspath(__file__)] + sys.argv[1:])

@bot.command()
async def stop(ctx):
    await ctx.send("Shutting down...")
    await bot.close()
    print(f'Shutting down by {ctx.author}...')

@bot.command()
async def ping(ctx):
    await ctx.send(f"latency: {round(bot.latency * 1000)}ms")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await sync_command_logic(bot)
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.custom,
            name="Eating cookie",
            details=".w.",
            state="Eating cookie",
        ),
        status=discord.Status.online
    )
   
    if not os.path.exists("taobao_state.json"):
        print("[!] taobao_state.json not found. Please log in to Taobao...")
        await polaroid_check.check_taobao_stock()
    
    print("[*] Starting stock check")
    check_stock_loop.start()


@bot.event
async def on_message(message):
    print(f"{message.content} - {message.author}")
    await bot.process_commands(message) 
    await handle_hdl(message) 

async def handle_hdl(message):
    if message.author == bot.user:
        return
    if "海底撈" in message.content:
        user_to_mention = discord.utils.get(message.guild.members, name=".nyx4695")
        await message.channel.send(f"{user_to_mention.mention} 所以我說海底撈呢")



awake()
bot.run(noi_token)