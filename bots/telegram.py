import os
import telepot, pymysql, reply
import util, glob

client = None  # asyncio client
bclient = None # blocking client

async def onMessage(msg):
	try:
		db = glob.db

		contentType, chatType, chatId = telepot.glance(msg)

		userInfo, chat = util.checkDatabase(msg['from'], chatId, chatId < 0, 't')
		
		if contentType == 'text':
			print('Telegram message from', userInfo['firstName'], userInfo['lastName'])
			print('\tChat ID:', chatId, '(Private)' if chatId >= 0 else '(Public)')
			print('\tMessage:', msg['text'], '\n')
		else:
			print('Message:', contentType, chatType, chatId, '(' + userInfo['firstName'], userInfo['lastName'] + ')')
			return

		origText = msg['text'].replace('@SamTheNerdBot', '')
		origText = origText[1:] if origText[0] == '/' else origText
		
		response = reply.getReply(chatId, origText, userInfo, chat)
		if response.strip():
			await client.sendMessage(chatId, response)
	except (ConnectionAbortedError, pymysql.err.OperationalError, pymysql.err.InterfaceError):
		await client.sendMessage(chatId, 'Connection lost to the database. Connecting...')
		db.close()
		db.open()
		await client.sendMessage(chatId, 'Connected!')
	except Exception as e:
		glob.messageAdmins('Uncaught Error: {}'.format(e))
		await client.sendMessage(chatId, 'Sorry, something went wrong... ')


async def onCallbackQuery(msg):
	pass


async def onInlineQuery(msg):
	pass


async def onInlineResult(msg):
	resultId, fromId, queryString = telepot.glance(msg, flavor='chosen_inline_result')

	if resultId == 'help':
		print('Wanted Help.')
		

def init():
	global client, bclient
	client = telepot.aio.Bot(os.environ['TELEGRAM_TOKEN'])
	bclient = telepot.Bot(os.environ['TELEGRAM_TOKEN'])
	
async def listen():
	await client.message_loop({
		'chat': onMessage,
		'callback_query': onCallbackQuery,
		'inline_query': onInlineQuery,
		'chosen_inline_result': onInlineResult
	})
