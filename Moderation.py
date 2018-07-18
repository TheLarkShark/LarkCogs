import discord
from discord.ext import commands
import random
import math
from random import randint
import json
import datetime
import asyncio
import time
from discord import User
from discord.ext.commands import Bot
from pypubg import core
from time import gmtime

client = discord.Client()


@commands.has_permissions(kick_members=True)
class Moderation():
    def __init__(self, bot):
        self.bot = bot

    @commands.group(no_pm=True)
    @commands.has_permissions(kick_members=True)
    async def modlog(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.bot.get_command('help'), 'modlog')

    @modlog.command(pass_context=True,no_pm=True)
    @commands.has_permissions(kick_members=True)
    async def set(self, ctx, channel: discord.TextChannel):
        'Sets the mod-log channel'
        await ctx.bot.default_channels.set_channel(ctx.guild, channel)
        await ctx.send("Mod-log channel set")
    
    @modlog.command(pass_context=True,no_pm=True)
    @commands.has_permissions(kick_members=True)
    async def get(self,ctx):
        'Returns the current mod-log channel'
        channel = await ctx.bot.default_channels.get_channel(ctx.guild)
        await ctx.send('<#{}>'.format(channel) if channel else 'None set')
    
    @client.event
    async def on_member_join(self,member):
        guild = member.guild
        channel_id = await self.bot.default_channels.get_channel(guild)
        embed = discord.Embed(title="User Joined", color=16721408)
        embed.set_thumbnail(url=member.avatar_url_as(format=None,static_format='webp',size=1024))
        embed.add_field(name='User:', value=member.mention, inline=True)
        embed.add_field(name="User ID:", value=member.id, inline=True)
        embed.add_field(name="Bot:", value=member.bot, inline=False)
        embed.add_field(name="Created At:", value=member.created_at, inline=True)
        embed.add_field(name="Joined At:", value=member.joined_at, inline=True)
        await guild.get_channel(channel_id).send(embed=embed)
    
    @client.event
    async def on_member_remove(self,member):
        guild = member.guild
        channel_id = await self.bot.default_channels.get_channel(guild)
        embed = discord.Embed(title="User Left", color=16721408)
        embed.set_thumbnail(url=member.avatar_url_as(format=None,static_format='webp',size=1024))
        embed.add_field(name='User:', value=member.mention, inline=True)
        embed.add_field(name="User ID:", value=member.id, inline=True)
        await guild.get_channel(channel_id).send(embed=embed)

    @commands.command(pass_context=True,no_pm=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason: str):
        'Kicks someone from the server'
        guild = ctx.guild
        author = ctx.author
        channel_id = await ctx.bot.default_channels.get_channel(ctx.guild)
        td = datetime.datetime.now()
        td = td.strftime('%m-%d-%Y, %I:%M:%S %p EST')
        embed = discord.Embed(title="User Kicked", color=16721408)
        embed.set_thumbnail(url=user.avatar_url_as(format=None,static_format='webp',size=1024))
        embed.add_field(name='User:', value=user.mention, inline=True)
        embed.add_field(name='Reason:', value=reason, inline=True)
        embed.add_field(name='Responsible Moderator:', value=author, inline=False)
        embed.set_footer(text=td)
        if reason is not None:
            await ctx.send('The boot has kicked.')
            try:
                await user.kick()
                await guild.get_channel(channel_id).send(content='User Kicked',embed=embed)
                await user.send(content='You have been kicked for ' + reason, tts=False, embed=None)
            except discord.errors.Forbidden:
                await ctx.send('Either I do not have permission, or you do not')
                return

    @commands.command(pass_context=True,no_pm=True)
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, user: discord.Member, *, reason: str):
        'Warns a user'
        guild = ctx.guild
        author = ctx.author
        channel_id = await ctx.bot.default_channels.get_channel(ctx.guild)
        td = datetime.datetime.now()
        td = td.strftime('%m-%d-%Y, %I:%M:%S %p EST')
        embed = discord.Embed(title="User Warned", color=16721408)
        embed.set_thumbnail(url=user.avatar_url_as(format=None,static_format='webp',size=1024))
        embed.add_field(name='User:', value=user.mention, inline=True)
        embed.add_field(name='Reason:', value=reason, inline=True)
        embed.add_field(name='Responsible Moderator:', value=author.mention, inline=False)
        embed.set_footer(text=td)
        if reason is not None:
            try:
                await guild.get_channel(channel_id).send(embed=embed)
                await user.send(content='You have been warned in {} for {}'.format(guild,reason), tts=False, embed=None)
            except discord.errors.Forbidden:
                await ctx.send('Either I do not have permission, or you do not')
                return

    @commands.command(pass_context=True,no_pm=True)
    @commands.has_permissions(kick_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason: str):
        'Bans someone from the server'
        guild = ctx.guild
        author = ctx.author
        channel_id = await ctx.bot.default_channels.get_channel(ctx.guild)
        td = datetime.datetime.now()
        td = td.strftime('%m-%d-%Y, %I:%M:%S %p EST')
        embed = discord.Embed(title="User Banned", color=16721408)
        embed.set_thumbnail(url=user.avatar_url_as(format=None,static_format='webp',size=1024))
        embed.add_field(name='User:', value=user.mention, inline=True)
        embed.add_field(name='Responsible Moderator:', value=author, inline=False)
        embed.set_footer(text=td)
        if reason is not None:
            await ctx.send('The ban hammer has spoken.')
            try:
                await user.ban()
                await guild.get_channel(channel_id).send(content='User Banned',embed=embed)
                await user.send(content='You have been banned from {} for {}'.format(guild,reason), tts=False, embed=None)
            except discord.errors.Forbidden:
                await ctx.send('Either I do not have permission, or you do not')
                return

    @commands.command(pass_context=True,no_pm=True)
    @commands.has_permissions(manage_messages=True)
    async def prune(self, ctx, number: int):
        'Deletes a set amount of messages'
        await ctx.channel.purge(limit=number + 1)

    @commands.command(pass_context=True,no_pm=True)
    @commands.has_permissions(manage_roles=True)
    async def assign(self, ctx, role: discord.Role = None, user: discord.Member = None):
        'Assigns a user a role'
        if role is None:
            return await ctx.send("You haven't specified a role! ")
        if role not in ctx.guild.roles:
            return await ctx.send("That role doesn't exist.")
        if user is None:
            if role not in ctx.author.roles:
                await ctx.author.add_roles(role)
                return await ctx.send('{} role has been added to {}.'.format(role, ctx.author.mention))
            if role in ctx.author.roles:
                await ctx.author.remove_roles(role)
                return await ctx.send('{} role has been removed from {}.'.format(role, ctx.author.mention))
        if role not in user.roles:
            await user.add_roles(role)
            return await ctx.send('{} role has been added to {}.'.format(role, user.mention))
        if role in user.roles:
            await user.remove_roles(role)
            return await ctx.send('{} role has been removed from {}.'.format(role, user.mention))

    @commands.command(pass_context=True,no_pm=True)
    @commands.has_permissions(manage_messages=True)
    async def log(self, ctx, number: int, channel: discord.TextChannel):
        'Logs past messages of a channel into a text file'
        async for message in channel.history(limit=number):
            output = ((((('```' + str(message.author)) + ' at ') + str(message.created_at)) + ': \n') + str(
                message.content)) + '\n```'
            await ctx.send(output)

    @commands.command(pass_context=True,no_pm=True)
    async def leave(self, ctx):
        'Makes the bot leave the server'
        await ctx.send("Bye I'll miss u bb")
        await ctx.guild.leave()

    @commands.command(pass_context=True,no_pm=True)
    async def bans(self, ctx):
        'Shows banned users of a server'
        x = await ctx.guild.bans()
        x = '\n'.join([y.name for y in x])
        embed = discord.Embed(title='List of Banned Members:', description=x, color=745822)
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
