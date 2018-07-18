# Used with permission via MIT License from stroupbslayen

import discord
from discord.ext import commands
import asyncio,aiohttp,json
from bs4 import BeautifulSoup as soup

modes = {
		'solo-tpp':{
			'name':'tpp','size':1},
		'duo-tpp':{
			'name':'tpp','size':2},
		'squad-tpp':{
			'name':'tpp','size':4},
		'solo-fpp':{
			'name':'fpp','size':1},
		'duo-fpp':{
			'name':'fpp','size':2},
		'squad-fpp':{
			'name':'fpp','size':4},
        'solo':{
			'name':'fpp','size':1},
		'duo':{
			'name':'fpp','size':2},
		'squad':{
			'name':'fpp','size':4}
		}

regions={
		'na':'[NA] North America',
		'as':'[AS] Asia',
		'sea':'[SEA] South East Asia',
		'krjp':'[KRJP] Korea/Japan',
		'oc':'[OC] Oceania',
		'sa':'[SA] South America',
		'eu':'[EU] Europe'
		}

class default:
	mode='solo-fpp'
	region='na'

class PUBG():
	def __init__(self,bot):
		 self.bot=bot

	async def no_player(self,ctx):
		embed=discord.Embed(title='Error', description='No player name was entered.',color=745822)
		await ctx.send(embed=embed)

	async def error_message(self,ctx,playername,message):
		embed= discord.Embed(title='Message from PUBG.OP.GG:', description='Error for player {}:\n{}'.format(playername,message),color=745822)
		await ctx.send(embed=embed)

	async def PUBG_API(self,url):
		try:
			async with aiohttp.get(url) as data:
				data=await data.json()
				return data
		except BaseException as error:
			print('Unhandled exception: ' + str(error))
			raise

	async def getID(self,playername):
		data= await aiohttp.get('https://pubg.op.gg/user/{}'.format(playername))
		data= await data.text()
		#get HTML of page
		page = soup(data,"html.parser")
		#get line with player ID
		pID=page.find('div',{'class':'player-summary__name'})
		if pID is None:
			return {'error':'Player not found'}
		playerid=pID['data-user_id']
		nickname=pID['data-user_nickname']
		#get line with current season
		season=page.find('a',{'class':'game-server__btn game-server__btn--on'})
		season=("2018-06")
		return {'playerid':playerid,'season':season,'nickname':nickname}

	@commands.command()
	async def stats(self,ctx,*,message:str=None):
		'Get stats for a PUBG player'
		await ctx.trigger_typing()
		mode=None
		region=None
		players=[]

		#message if no data is entered
		if message==None:
			msg=await ctx.no_player()
			return

		message = message.lower().split()

		#get player region and match type, if none are put in it uses default values
		for data in message:
			if data in modes:
				mode=data
			if data in regions:
				region=data
			if data not in (list(modes)+list(regions)):
				players.append(data)

		#sets search criteria if none is input, uses default values
		if mode==None:
			mode=default.mode
		if region==None:
			region=default.region

		#check if playernames are entered
		if len(players)==0:
			await ctx.send("You haven't specified a player!")

		else:
			for player in players:
				data = await self.getID(player)
				if 'error' not in data:
					class profile:
						nickname=data['nickname']
						playerid=data['playerid']
						season=data['season']
						server=region
						match=modes[mode]['name']
						size=modes[mode]['size']
					url='https://pubg.op.gg/api/users/{0.playerid}/ranked-stats?season={0.season}&server={0.server}&queue_size={0.size}&mode={0.match}'.format(profile)
					player_stats = await self.PUBG_API(url)
					if 'message' in player_stats:
						await self.bot.error_message(profile.nickname,'Player has no stats for {}-{}'.format(regions[region],mode.upper()))
					else:
						embed = discord.Embed(title=profile.nickname,url='https://pubg.op.gg/user/{0.nickname}?server={0.server}'.format(profile), description='{}-{}\nGrade: **{}**\nSeason: {}'.format(regions[region],mode.upper(),player_stats['grade'],profile.season) , color=745822)
						embed.add_field(name="Rank", value=player_stats['ranks']['rating'], inline=True)
						embed.add_field(name="Skill Rating", value=player_stats['stats']['rating'], inline=True)
						embed.add_field(name="Wins",value=player_stats['stats']['win_matches_cnt'], inline=True)
						embed.add_field(name="Win Rate", value='{}%'.format(round(player_stats['stats']['win_matches_cnt']/player_stats['stats']['matches_cnt']*100,2), inline=True))
						embed.add_field(name='Kills', value=player_stats['stats']['kills_sum'],inline=True)
						embed.add_field(name="K/D", value=round(player_stats['stats']['kills_sum']/player_stats['stats']['deaths_sum'],2), inline=True)
						await ctx.send(embed=embed)
				else:
					error=await self.bot.error_message(player,data['error'])


def setup(bot):
	bot.add_cog(PUBG(bot))
