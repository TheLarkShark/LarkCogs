import discord
from discord.ext import commands
import random
import math
from random import randint
import datetime
import asyncio
import time
import pyowm
import aiohttp
from discord import User
from discord.ext.commands import Bot
from time import gmtime
from pypubg import core
from weather import Weather, Unit

client = discord.Client()


class Utility():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def calc(self, ctx, left: float, operation: str, right: float):
        "It's a calculator!"
        if operation == '+':
            await ctx.send(left + right)
        elif operation == '-':
            await ctx.send(left - right)
        elif (operation == '*') or (operation == 'x'):
            await ctx.send(left * right)
        elif (operation == '/') or (operation == '÷'):
            await ctx.send(left / right)
        elif operation == '^':
            await ctx.send(math.pow(left, right))
        else:
            await ctx.send('Try again.')

    @commands.command(pass_context=True)
    async def joined(self, ctx, member: discord.Member = None):
        'Says when a member joined.'
        author = ctx.author
        if member is None:
            await ctx.send('{0.mention} joined on {0.joined_at}'.format(author))
        else:
            await ctx.send('{0.mention} joined on {0.joined_at}'.format(member))

    @commands.command(pass_context=True)
    async def pubgstats(self, ctx, pubgplayer: str):
        'Shows PUBG Stats (NOT WORKING ATM)'
        api = core.PUBGAPI('fa1607e6-538f-4c4d-96e1-5347c9163aaa')
        await ctx.send(api.player(pubgplayer))

    @commands.command(pass_context=True)
    async def avatar(self, ctx, user: discord.User = None):
        "Shows a user's avatar"
        if user is None:
            await ctx.send(ctx.author.avatar_url)
        elif user is not None:
            await ctx.send(user.avatar_url)
        else:
            await ctx.send('User does not have an avatar')

    @commands.command(pass_context=True)
    async def rolecolor(self, ctx, role: discord.Role):
        'Returns the color of a role'
        await ctx.send(role.colour)

    @commands.group(pass_context=True,no_pm=True)
    async def info(self, ctx):
        'Returns some info'
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.bot.get_command('help'), 'info')
            return

    @info.command(pass_context=True,no_pm=True)
    async def server(self, ctx):
        'Returns some neat server info'
        guild=ctx.guild
        embed = discord.Embed(title=guild.name, color=745822)
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name='Region:', value=guild.region, inline=True)
        embed.add_field(name='Verification Level:', value=guild.verification_level, inline=True)
        embed.add_field(name='Owner:', value=guild.owner, inline=True)
        embed.add_field(name='Number of Members:', value=guild.member_count, inline=True)
        embed.add_field(name='Server ID:', value=guild.id, inline=True)
        embed.add_field(name='Created At:', value=guild.created_at, inline=True)
        await ctx.send(embed=embed)

    @info.command(pass_context=True,no_pm=True)
    async def user(self, ctx, member: discord.Member = None):
        'Returns some nifty user info'
        author=ctx.author
        roles_string = ''
        for obj1 in author.roles:
            roles_string = (roles_string + '\n') + obj1.name
        if member is None:
            embed = discord.Embed(title=author.name, color=745822)
            embed.set_thumbnail(url=ctx.author.avatar_url_as(format=None,static_format='webp',size=1024))
            embed.add_field(name='User ID:', value=author.id, inline=True)
            embed.add_field(name='Status:', value=author.status, inline=True)
            embed.add_field(name='Roles:', value=roles_string, inline=False)
            embed.add_field(name='Created At:', value=author.created_at, inline=True)
            embed.add_field(name='Joined Server At:', value=author.joined_at, inline=True)
            await ctx.send(embed=embed)
        membroles = member.roles
        membroles_string = ''
        for obj2 in membroles:
            membroles_string = (membroles_string + '\n') + obj2.name
        else:
            embed = discord.Embed(title=member.display_name, color=745822)
            embed.set_thumbnail(url=member.avatar_url_as(format=None,static_format='webp',size=1024))
            embed.add_field(name='User ID:', value=member.id, inline=True)
            embed.add_field(name='Status:', value=member.status, inline=True)
            embed.add_field(name='Roles:', value=membroles_string, inline=False)
            embed.add_field(name='Created At:', value=member.created_at, inline=True)
            embed.add_field(name='Joined Server At:', value=member.joined_at, inline=True)
            await ctx.send(embed=embed)

    @info.command(pass_context=True,no_pm=True)
    async def tchannel(self, ctx, text_channel: discord.TextChannel = None):
        'Returns info about a text channel'
        name = ctx.channel.name
        channelid = ctx.channel.id
        ctopic = ctx.channel.topic
        createdat = ctx.channel.created_at
        avatarurl = ctx.guild.icon_url
        if text_channel is None:
            embed = discord.Embed(title=name, color=745822)
            embed.set_thumbnail(url=avatarurl)
            embed.add_field(name='Topic:', value=ctopic, inline=False)
            embed.add_field(name='Channel ID:', value=channelid, inline=True)
            embed.add_field(name='Created At:', value=createdat, inline=True)
            await ctx.send(embed=embed)
        elif text_channel is not None:
            embed = discord.Embed(title=text_channel.name, color=745822)
            embed.set_thumbnail(url=avatarurl)
            embed.add_field(name='Topic:', value=text_channel.topic, inline=False)
            embed.add_field(name='Channel ID:', value=text_channel.id, inline=True)
            embed.add_field(name='Created At:', value=text_channel.created_at, inline=True)
            await ctx.send(embed=embed)
    
    @info.command()
    async def vchannel(self,ctx,*, voice_channel:discord.VoiceChannel):
        'Returns info about a voice channel'
        embed = discord.Embed(title=voice_channel.name, color=745822)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name='Channel ID:', value=voice_channel.id, inline=False)
        embed.add_field(name='Bitrate:', value=voice_channel.bitrate, inline=True)
        embed.add_field(name='Maximum Members:', value=voice_channel.user_limit, inline=True)
        embed.add_field(name='Created At:', value=voice_channel.created_at, inline=True)
        await ctx.send(embed=embed)
    
    @info.command()
    async def emoji(self,ctx,emoji:discord.Emoji):
        'Returns some emote-tastic emoji info. Must be a custom emoji from a server the bot is part of.'
        embed=discord.Embed(title=emoji.name, color=745822)
        embed.set_thumbnail(url=emoji.url)
        embed.add_field(name='Emoji ID:', value=emoji.id, inline=True)
        embed.add_field(name='Created At:', value=emoji.created_at, inline=True)
        embed.add_field(name='Home Server:', value=emoji.guild, inline=False)
        embed.add_field(name='Animated:', value=emoji.animated, inline=True)
        embed.add_field(name='Twitch Emote:', value=emoji.managed, inline=True)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def weather(self, ctx, *, loc: str):
        'Returns weather info'
        weather = Weather(unit=Unit.FAHRENHEIT)
        location = weather.lookup_by_location(loc)
        condition = location.condition
        embed = discord.Embed(title='Weather in {}:'.format(loc), color=745822)
        embed.add_field(name='Temperature:', value=condition.temp + '°F', inline=True)
        embed.add_field(name='Condition:', value=condition.text, inline=True)
        embed.set_footer(text='Powered by Yahoo! Weather')
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def time(self, ctx, *, place):
        'Shows what time it is in other places'
        async with aiohttp.get('https://timezoneapi.io/api/address/?{}'.format(place)) as response:
            data = await response.json()
        if data['data']['addresses_found'] != '0':
            City = data['data']['addresses'][0]['formatted_address']
            FullDay = data['data']['addresses'][0]['datetime']['day_full']
            Month = data['data']['addresses'][0]['datetime']['month_full']
            Day = data['data']['addresses'][0]['datetime']['day']
            Year = data['data']['addresses'][0]['datetime']['year']
            Hour = data['data']['addresses'][0]['datetime']['hour_12_wolz']
            Minute = data['data']['addresses'][0]['datetime']['minutes']
            Second = data['data']['addresses'][0]['datetime']['seconds']
            AP = data['data']['addresses'][0]['datetime']['hour_am_pm']
            TZ = data['data']['addresses'][0]['datetime']['offset_tzfull']
            embed = discord.Embed(
                title=City,
                description='{}, {} {}, {} at {}:{}:{} {}\n{}'.format(FullDay, Month, Day, Year, Hour, Minute, Second, AP.upper(), TZ),
                color=745822)
            embed.set_footer(text='Powered by Timezoneapi.io')
            await ctx.send(embed=embed)
        if data['data']['addresses_found'] == '0':
            await ctx.invoke(ctx.get_command('help'), 'time')
    
    @commands.command()
    async def servers(self,ctx):
        'Lists all the servers the bot is in'
        guilds = list(self.bot.guilds)
        await ctx.send("I'm in {} servers".format(str(len(self.bot.guilds))))
        for x in range (len(guilds)):
            await ctx.send(" {} - {}".format(guilds[x-1].name,guilds[x-1].id))


def setup(bot):
    bot.add_cog(Utility(bot))
