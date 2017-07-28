import os, sys, time, random, hashlib, asyncio, subprocess, threading, requests, json, re
import util, reminders, glob
import telepot, pymysql

from glob import message, m, tryFiller
from reply import genReply, tests, filler
from expressions import ExpressionSolver, ExpressionTree, InfixToPostfix
from database import Database
from emoji import Emoji

##################################################################################################
##################################################################################################
# Utility Functions

def addUser(info, chat):
	if (info['id'], chat) not in glob.chatUsers:
		print('Adding Chat User: ' + str(chat) + ': ' + str(info['id']))
		glob.db.addChatUser(chat, info['id'])
		glob.chatUsers[(info['id'], chat)] = True
	if chat not in glob.chats:
		print('Adding Chat: ' + str(chat))
		glob.db.addChat(chat)
		glob.chats[chat] = True
	if info['id'] not in glob.users:
		print('Adding User: ' + str(info['id']))
		glob.db.addUser(info['id'], info['username'], info['first_name'], info['last_name'])
		glob.users[info['id']] = True

##################################################################################################
##################################################################################################

async def onMessage(msg):
	db = glob.db
	try:
		db.testConnection()

		contentType, chatType, chatId = telepot.glance(msg)
		userInfo = msg['from']
		print('Chat:', contentType, chatType, chatId)

		addUser(userInfo, chatId)

		if contentType != 'text':
			return

		text = msg['text']

		waitingFor = db.getWaitingFor(userInfo['id'])['waitingFor']
		if waitingFor == 'call':
			db.setWaitingFor(userInfo['id'], 'nothing')
			db.setNickname(userInfo['id'], text)
			await message(chatId, 'callmesuccess', userInfo, text)
			return
		elif waitingFor == 'like':
			db.setWaitingFor(userInfo['id'], 'nothing')
			db.addLike(userInfo['id'], text)
			await message(chatId, 'ilike', userInfo, text)
			return
		elif waitingFor == 'dislike':
			db.setWaitingFor(userInfo['id'], 'nothing')
			db.removeLike(userInfo['id'], text)
			await message(chatId, 'idontlike', userInfo, text)
			return

		text = text[1:] if text[0] == '/' else text
		text.replace('@SamTheNerdBot', '')
		origText = text
		text = text.lower()

		if text.startswith('say'):
			glob.say(text[3:])
		elif text.startswith('calc'):
			try:
				e = ExpressionSolver(text[4:])
				ans = e.solve()
			except:
				await m(chatId, 'Sorry, I can\'t solve that.')
			else:
				if ans == 42:
					await message(chatId, '42', userInfo)
				else:
					await m(chatId, 'Answer: ' + str(ans))
		elif text.startswith('infix'):
			i = InfixToPostfix(text[5:].strip())
			try:
				await m(chatId, 'Postfix: ' + i.genPostfix())
			except:
				await m(chatId, 'Error parsing infix expression.')
		elif text.startswith('postfix'):
			try:
				e = ExpressionTree(text[7:].strip())
				await m(chatId, 'Answer: ' + str(e.eval()))
			except:
				await m(chatId, 'Error parsing postfix expression.')
		elif 'valid' in text:
			if random.randint(1, 10) == 5:
				await glob.bot.sendPhoto(chatId, open('tim.png', 'rb'))
			elif random.randint(1, 4) == 2:
				for i in range(5):
					await m(chatId, 'valid')
					await asyncio.sleep(1)
			else:
				await message(chatId, 'valid', userInfo)
		elif text.startswith('meme'):
			await glob.bot.sendPhoto(chatId, open('tim.png', 'rb'))
		elif text.startswith('ls'):
			ans = ['Files in current directory: ', '']
			for file in os.listdir('.'):
				ans.append(file)
			await m(chatId, '\n'.join(ans))
		elif text.startswith('cat '):
			fileName = origText[4:]
			try:
				with open(fileName) as file:
					contents = file.read().replace(TOKEN, '{{HIDDEN INFORMATION}}')
					await m(chatId, contents)
			except FileNotFoundError:
				await m(chatId, 'Could not find "{}"'.format(fileName))
			except:
				await m(chatId, 'Unknown Error')
		elif text.startswith('echo '):
			await m(chatId, text[5:])
		elif text.startswith('call me') or text.startswith('callme'):
			newName = origText[origText.lower().index('me')+2:].strip()
			if newName != '':
				db.setNickname(userInfo['id'], newName)
				await m(chatId, 'Okay, from now on, I\'ll call you ' + newName + '! ' + Emoji.happy())
			else:
				db.setWaitingFor(userInfo['id'], 'call')
				await message(chatId, 'callme', userInfo)
		elif text.startswith('time'):
			await m(chatId, str(util.getDate()))
		elif text.startswith('tim'):
			if random.randint(1, 10) == 5:
				await glob.bot.sendVideo(chatId, open('tim.mov', 'rb'))
			else:
				await message(chatId, 'tim', userInfo)
		elif '\U0001f611' in text:
			await message(chatId, 'annoying', userInfo)
		elif text.startswith('hi') or text.startswith('hey') or text.startswith('hello'):
			user = db.getUser(userInfo['id'])
			if user['nickName'] != None:
				if user['nickName'].lower() == 'bae':
					await message(chatId, 'bae', userInfo)
				else:
					await message(chatId, 'hello', userInfo, user['nickName'])
			else:
				await message(chatId, 'hello', userInfo, user['nickName'])
		elif text.startswith('emoji'):
			await m(chatId, chr(random.randint(0x1F601, 0x1F650)))
		elif text.startswith('gravatar'):
			email = text[8:].strip()
			md5 = hashlib.md5()
			m.update(email.encode('utf-8'))
			await glob.bot.sendPhoto(chatId, 'https://www.gravatar.com/avatar/' + md5.hexdigest() + '.jpg')
		elif text.startswith('rand'):
			data = text.split()
			if len(data) != 3:
				await m(chatId, 'Format should be \"rand [num1] [num2]\".')
			else:
				try:
					await m(chatId, random.randint(int(data[1]), int(data[2])))
				except:
					await m(chatId, 'Please enter a valid number.')
		elif text.startswith('python'):
			cmd = text[6:]
			if 'quit' not in cmd and 'exit' not in cmd and 'sigterm' not in cmd and 'kill' not in cmd:
				try:
					await m(chatId, eval(cmd))
				except:
					await m(chatId, 'Error parsing Python code.')
			else:
				await m(chatId, 'You cannot shut me down.')
		elif 'emotion' in text:
			await message(chatId, 'emotion', userInfo)
		elif text.startswith('i like') or text.startswith('ilike'):
			like = origText[text.index('like')+4:].strip()
			if like != '':
				db.addLike(userInfo['id'], like)
				await message(chatId, 'ilike', userInfo, like)
			else:
				db.setWaitingFor(userInfo['id'], 'like')
				await m(chatId, 'What do you like, ' + userInfo['first_name'] + '?')
		elif text.startswith('i dont like') or text.startswith('idontlike') or text.startswith('i don\'t like'):
			like = origText[text.index('like')+4:].strip()
			if like != '':
				db.removeLike(userInfo['id'], like)
				await message(chatId, 'idontlike', userInfo, like)
			else:
				db.setWaitingFor(userInfo['id'], 'dislike')
				await m(chatId, 'What do you not like, ' + userInfo['first_name'] + '?')
		elif text.startswith('likes'):
			likes = db.getLikes(userInfo['id'])
			if len(likes) == 0:
				await m(chatId, 'I don\'t know what you like!')
			else:
				await m(chatId, 'You like ' + str(', '.join(likes)))
		elif 'noice' in text:
			await glob.bot.sendPhoto(chatId, 'http://www.vomzi.com/wp-content/uploads/2016/02/new-noice-gif-777.gif')
		elif text.startswith('locate'):
			r = requests.get('http://freegeoip.net/json')
			j = json.loads(r.text)
			await glob.bot.sendLocation(chatId, j['latitude'], j['longitude'])
		elif '\U0001f602' in text:
			await m(chatId, '\U0001f602' * random.randint(1, 5))
		elif text.startswith('weather'):
			try:
				await m(chatId, 'Calculating...')
				r = requests.get('http://freegeoip.net/json')
				j = json.loads(r.text)
				weather = owm.weather_around_coords(j['latitude'], j['longitude'])[0].get_weather()
				temp = weather.get_temperature('fahrenheit')['temp']
				clouds = weather.get_clouds()
				humid = weather.get_humidity()
				status = weather.get_detailed_status()
				if temp <= 32: # Cold!
					await message(chatId, 'freezing', userInfo, status, str(temp), str(clouds), str(humid))
				elif temp <= 60: # Cool and Nice
					await message(chatId, 'cool', userInfo, status, str(temp), str(clouds), str(humid))
				elif temp <= 85: # Warm and Nice
					await message(chatId, 'warm', userInfo, status, str(temp), str(clouds), str(humid))
				else: #Hot
					await message(chatId, 'hot', userInfo, status, str(temp), str(clouds), str(humid))
			except:
				await m(chatId, 'Couldn\'t get the weather... Try Again?')
		elif not await reminders.tryParse(text, origText, chatId, userInfo):
			for k, v in tests.items():
				if v != 'manual' and eval(v):
					if k in filler:
						await tryFiller(chatId, userInfo)
					await message(chatId, k, userInfo)
					return
	except ConnectionAbortedError:
		await m(chatId, 'Connection lost to the database. Connecting...')
		db.close()
		db.open()
		await m(chatId, 'Connected!')
	except pymysql.err.OperationalError:
		await m(chatId, 'Connection lost to the database. Connecting...')
		db.close()
		db.open()
		await m(chatId, 'Connected!')
	except Exception as e:
		await m(chatId, 'Uncaught Error: ' + str(e))


##################################################################################################
##################################################################################################

async def onCallbackQuery(msg):
	pass

##################################################################################################
##################################################################################################

async def onInlineQuery(msg):
	pass

##################################################################################################
##################################################################################################

def onInlineResult(msg):
	resultId, fromId, queryString = telepot.glance(msg, flavor='chosen_inline_result')

	if resultId == 'help':
		print('Wanted Help.')