import os, sys, random, asyncio
import telepot.aio, pyowm, pyttsx3, pyaudio
import database, reply, hotword

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
OWM_TOKEN = os.environ['OWM_TOKEN']
ADMIN_ID = os.environ['ADMIN_ID']
ESPEAK_OPTIONS = ['espeak', '-ven-us+f3', '-s170']
pause = False
bot = answerer = db = owm = speech = None
users = {}
chats = {}
chatUsers = {}
speechQueue = []

def init():
	global bot, answerer, db, owm, users, chat, chatUsers, speech
	print('\n' + '-' * 50)
	print('Initializing in Production Mode...')
	print('-' * 50)
	print('Loading Telegram Bot...')
	bot = telepot.aio.Bot(TELEGRAM_TOKEN)
	answerer = telepot.aio.helper.Answerer(bot)
	print('Done!\n')
	print('Loading Database...')
	db = database.Database()
	db.loadUsers(users)
	db.loadChats(chats)
	db.loadChatUsers(chatUsers)
	print('Done!\n')
	print('Loading OWM...')
	owm = pyowm.OWM(OWM_TOKEN)
	print('Done!\n')
	print('Initializing Speech Engine...')
	speech = pyttsx3.init()
	speech.setProperty('rate', 150)
	print('Done!\n')
	print('Initializing Microphone...')
	hotword.init()
	print('Done!')
	print('-' * 50 + '\n')

async def m(chatId, text):
	global bot, speech
	await bot.sendMessage(chatId, text)

def say(message):
	global speechQueue
	speechQueue.append(message)

def cleanup():
	global db
	db.close()
