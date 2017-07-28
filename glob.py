import os, sys, random, asyncio
import telepot.aio, pyowm, pyttsx3
import database, reply

TOKEN = '265155953:AAFp_YxsPmVO8N4k6y6fkPIyXKBcumnif8Y'
bot = answerer = db = owm = speech = None
users = chats = chatUsers = {}

def init():
	global bot, answerer, db, owm, speech, users, chat, chatUsers
	print('\n' + '-' * 50)

	if len(sys.argv) == 2 and sys.argv[1] == 'DEBUG': # Debug Mode?
		os.environ['DEBUG'] = 'true'
		print('Initializing in Debug Mode...')
	else:
		os.environ['DEBUG'] = 'false'
		print('Initializing in Production Mode...')

	print('-' * 50 + '\n')
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
	print('Loading Speech Engine...')
	speech = pyttsx3.init()
	print('Done!\n')

async def message(chatId, text, userInfo, *args):
	global bot, speech
	message = reply.genReply(text, userInfo, *args)
	await bot.sendMessage(chatId, message)
	speech.say(message)

async def m(chatId, text):
	global bot, speech
	await bot.sendMessage(chatId, text)
	speech.say(text)

async def tryFiller(chatId, userInfo):
	if(random.randint(0, 3) == 2):
		await message(chatId, 'filler', userInfo)
		await asyncio.sleep(random.randint(1, 4))

def cleanup():
	global db
	db.close()