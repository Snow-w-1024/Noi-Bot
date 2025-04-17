import discord
from discord.ext import commands

def register_discussion_commands(bot):
    @bot.hybrid_command()
    async def create_thread(ctx, commodity_name: str):
        """
        為商品建立討論串
        """
        thread = await ctx.channel.create_thread(
            name=f"討論：{commodity_name}",
            type=discord.ChannelType.public_thread
        )
        await ctx.send(f"已為 {commodity_name} 建立討論串！")