import discord
from discord.ext import commands

def register_transaction_commands(bot):
    @bot.hybrid_command()
    async def trade(ctx, buyer: discord.Member, commodity_name: str, price: float):
        """
        記錄交易資訊
        """
        await ctx.send(f"交易記錄：\n商品：{commodity_name}\n買家：{buyer.mention}\n價格：${price}")