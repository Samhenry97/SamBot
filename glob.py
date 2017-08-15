import os, sys, random, asyncio, logging
import telepot.aio, pyowm, pyaudio
import database, reply, hotword, facebook

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
OWM_TOKEN = os.environ['OWM_TOKEN']
ADMIN_ID = int(os.environ['ADMIN_ID'])
ESPEAK_OPTIONS = ['espeak', '-ven-us+f3', '-s170']
pause = False
bot = answerer = db = owm = speech = None
users = {}
chats = {}
speechQueue = []

def init():
	if len(sys.argv) < 2 or sys.argv[1] != 'DEBUG':
		logging.basicConfig(level=logging.ERROR)
		logging.getLogger().setLevel(logging.ERROR)
	
	global bot, answerer, db, owm, users, chat, chatUsers, speech
	print('\n' + '-' * 50)
	print('Initializing in Production Mode...')
	print('-' * 50)
	print('Loading Telegram Bot...')
	bot = telepot.aio.Bot(TELEGRAM_TOKEN)
	answerer = telepot.aio.helper.Answerer(bot)
	print('Done!\n')
	print('Loading Facebook Bot...')
	facebook.init()
	print('Done!\n')
	print('Loading Database...')
	db = database.Database()
	db.loadUsers(users)
	db.loadChats(chats)
	print('Done!\n')
	print('Loading OWM...')
	owm = pyowm.OWM(OWM_TOKEN)
	print('Done!\n')
	print('Initializing Microphone...')
	hotword.init()
	print('Done!')
	print('-' * 50 + '\n')

async def m(chatId, text, type):
	global bot, speech
	if type == 't':
		await bot.sendMessage(chatId, text)
	elif type == 'm':
		facebook.client.sendMessage(text, thread_id=str(chatId))
		
def changeNickname(newName, chatId, userInfo):
	if userInfo['type'] == 'm':
		facebook.client.changeNickname(newName, str(userInfo['userId']), str(chatId))
	db.setNickname(userInfo['id'], newName)

def say(message):
	global speechQueue
	speechQueue.append(message)

def cleanup():
	global db
	db.close()
