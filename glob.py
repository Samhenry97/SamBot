import os, sys, random, asyncio
import telepot.aio, pyowm, pyttsx3
import database, reply

TOKEN = '265155953:AAFp_YxsPmVO8N4k6y6fkPIyXKBcumnif8Y'
ADMIN_ID = 131453030
bot = answerer = db = owm = speech = None
users = chats = chatUsers = {}
speechQueue = []

def init():
	global bot, answerer, db, owm, users, chat, chatUsers, speech
	print('\n' + '-' * 50)
	print('Initializing in Production Mode...')
	print('-' * 50)
	print('Loading Bot...')
	bot = telepot.aio.Bot(TOKEN)
	answerer = telepot.aio.helper.Answerer(bot)
	print('Done!\n')
	print('Loading Database...')
	db = database.Database()
	db.loadUsers(users)
	db.loadChats(chats)
	db.loadChatUsers(chatUsers)
	print('Done!\n')
	print('Loading OWM...')
	owm = pyowm.OWM('b1b2ccf3530eb007cdf6653fb6e71c0e')
	print('Done!\n')
	print('Initializing Speech Engine...')
	speech = pyttsx3.init()
	speech.setProperty('rate', 150)
	print('Done!')
	print('-' * 50 + '\n')

async def message(chatId, text, userInfo, *args):
	global bot, speech
	message = reply.genReply(text, userInfo, *args)
	await bot.sendMessage(chatId, message)

async def m(chatId, text):
	global bot, speech
	await bot.sendMessage(chatId, text)

def say(message):
	global speechQueue
	speechQueue.append(message)

def cleanup():
	global db
	db.close()
