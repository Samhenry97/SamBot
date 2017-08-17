import os
import util, glob
import telepot, pymysql
from reply import getReply

bot = None  # asyncio bot
bbot = None # blocking bot

##################################################################################################
##################################################################################################

async def onMessage(msg):
	try:
		db = glob.db

		contentType, chatType, chatId = telepot.glance(msg)

		userInfo = util.checkDatabase(msg['from'], chatId, chatId < 0, 't')
		
		if contentType == 'text':
			print('Telegram message from', userInfo['firstName'], userInfo['lastName'])
			print('\tChat ID:', chatId, '(Private)' if chatId >= 0 else '(Public)')
			print('\tMessage:', msg['text'], '\n')
		else:
			print('Message:', contentType, chatType, chatId, '(' + userInfo['firstName'], userInfo['lastName'] + ')')
			return

		origText = msg['text'].replace('@SamTheNerdBot', '')
		origText = origText[1:] if origText[0] == '/' else origText
		
		response = getReply(chatId, origText, userInfo)
		if response.strip():
			await bot.sendMessage(chatId, response)
	except (ConnectionAbortedError, pymysql.err.OperationalError, pymysql.err.InterfaceError):
		await bot.sendMessage(chatId, 'Connection lost to the database. Connecting...')
		db.close()
		db.open()
		await bot.sendMessage(chatId, 'Connected!')
	except Exception as e:
		print('Uncaught Error:', e)
		await bot.sendMessage(chatId, 'Sorry, something went wrong... ')

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

async def onInlineResult(msg):
	resultId, fromId, queryString = telepot.glance(msg, flavor='chosen_inline_result')

	if resultId == 'help':
		print('Wanted Help.')
		
##################################################################################################
##################################################################################################

def init():
	global bot, bbot
	bot = telepot.aio.Bot(os.environ['TELEGRAM_TOKEN'])
	bbot = telepot.Bot(os.environ['TELEGRAM_TOKEN'])
