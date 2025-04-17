import discord
from discord.ext import commands
from discord import app_commands

def register_commodity_image_commands(bot):
    
    @bot.hybrid_command()
    async def create_commodity(ctx, name: str, description: str, *, note: str = None, image: discord.Attachment = None):
        """
        Create a commodity with an image, description, and optional note.
        """
        # Check for an attached image
        image_url = None
        if ctx.message.attachments:
            image = ctx.message.attachments[0]
            if image.content_type.startswith("image/"):
                image_url = image.url
            else:
                await ctx.send("The attached file is not a valid image. Skipping the image.")

        # Send the commodity message
        embed = discord.Embed(title=name, description=description, color=discord.Color.blue())
        if image_url:
            embed.set_image(url=image_url)
        if note:
            embed.add_field(name="Note", value=note, inline=False)
        commodity_message = await ctx.send(embed=embed)

        # Create a discussion thread
        thread = await commodity_message.create_thread(name=f"Discussion: {name}")
        await ctx.send(f"Commodity '{name}' created with a discussion thread: {thread.mention}")

    @bot.hybrid_command()
    async def delete_commodity(ctx, commodity_name: str):
        """
        Delete a commodity message and its thread by commodity name.
        """
        try:
            # Fetch the message by matching the commodity name
            async for message in ctx.channel.history(limit=100):
                if message.author == ctx.guild.me and message.embeds:
                    embed = message.embeds[0]
                    if embed.title == commodity_name:
                        # Delete the thread (if it exists)
                        if message.thread:  # Check if the message has an associated thread
                            await message.thread.delete()

                        # Delete the message 
                        await message.delete()
                        await ctx.send(f"Commodity '{commodity_name}' has been deleted!")
                        return

            await ctx.send(f"Commodity with name '{commodity_name}' not found!")
        except discord.NotFound:
            await ctx.send(f"An error occurred while trying to delete '{commodity_name}'.")

    @bot.hybrid_command()
    async def list_commodities(ctx):
        """
        List all commodities in the current channel.
        """
        async for message in ctx.channel.history(limit=100):
            if message.author == ctx.guild.me and message.embeds:
                embed = message.embeds[0]
                if embed.title:
                    await ctx.send(f"Commodity: {embed.title}")



