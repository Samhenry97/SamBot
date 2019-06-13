from threading import Thread
import asyncio
import discord, glob, util, reply

client = None


class DiscordBot(discord.Client):
	async def on_ready(self):
		pass
	
	async def on_message(self, message):
		if message.author == self.user:
			return
		
		try:
			db = glob.db
			db.testConnection()
			
			author = message.author
			channel = message.channel
			public = type(channel) != discord.DMChannel
			userId = int(author.id)
			chatId = int(channel.id)
			user = db.getUser(userId, 'd')
			if user:
				info = { 'id': userId, 'first_name': user['firstName'], 'last_name': user['lastName'], 'username': user['userName'] }
			else:
				info = { 'id': userId, 'first_name': author.name, 'last_name': author.discriminator, 'username': author.name }
				
			userInfo, chat = util.checkDatabase(info, chatId, public, 'd')
			
			print('Discord message from', userInfo['firstName'], userInfo['lastName'])
			print('\tChat ID:', chatId, '(Public)' if public else '(Private)')
			print('\tMessage:', message.content, '\n')
			
			response = reply.getReply(message.content, userInfo, chat)
			if response.strip():
				await channel.send(response)
		except (ConnectionAbortedError, pymysql.err.OperationalError, pymysql.err.InterfaceError):
			await channel.send('Connection lost to the database. Connecting...')
			db.close()
			db.open()
			await channel.send('Connected!')
		except Exception as e:
			glob.messageAdmins('Uncaught Error: {}'.format(e))
			await channel.send('Sorry, something went wrong... ')
		
async def sendMessage(chatId, text):
	channel = client.get_channel(int(chatId))
	await channel.send(text)
		
def init():
	global client
	client = DiscordBot()
	
async def listen():
	await client.start('NTg4NTM1MzUxMjIwMzcxNDY4.XQGk6g.P5OV4P0qsn4Hy8GCcTgxt3PPxrs')
