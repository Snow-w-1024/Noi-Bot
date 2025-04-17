import discord
import datetime
def register_commands(bot):

    @bot.hybrid_command()  
    async def cookie(ctx):
        '''
        COOKIE!!! 
        '''
        message = await ctx.send("Cookie!")
        await message.add_reaction(":PaimonCookies:1354640670383669378")


    @bot.hybrid_command()  
    async def annoy(ctx, member: discord.Member):
        '''
        IDK what this command uses for but it's fun
        '''
        await ctx.send(f'{member.mention}')

    @bot.hybrid_command()
    async def say(ctx, message: str, channel: discord.TextChannel = None):
        '''
        say something in a certain channel 
        '''
        channel = channel or ctx.channel
        await channel.send(message)

    @bot.hybrid_command()
    async def join(ctx, channel: discord.VoiceChannel = None):
        '''
        have a party with Noi
        '''
        channel = channel or ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f'Joined {channel.name}')

