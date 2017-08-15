import util, glob
import telepot, pymysql

from glob import m
from reply import getReply
from emoji import Emoji

##################################################################################################
##################################################################################################

async def onMessage(msg):
	db = glob.db
	try:
		db.testConnection()

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
			await m(chatId, response, 't')
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
		print('Uncaught Error:', e)
		await m(chatId, 'Sorry, something went wrong... ' + Emoji.sad())

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
