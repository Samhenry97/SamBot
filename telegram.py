import os, sys, time, random, hashlib, asyncio, subprocess, threading, requests, json, re
import util, glob
import telepot, pymysql

from glob import message, m
from reply import getReply, tests, loadReplies

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
		
def processOutput(command):
	p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	return out.decode('utf-8') + err.decode('utf-8')

##################################################################################################
##################################################################################################

async def onMessage(msg):
	db = glob.db
	try:
		db.testConnection()

		contentType, chatType, chatId = telepot.glance(msg)
		userInfo = msg['from']
		print(userInfo)

		addUser(userInfo, chatId)

		if contentType == 'text':
			print('Message from', userInfo['first_name'], userInfo['last_name'])
			print('\tChat ID:', chatId, '(Private)' if chatId >= 0 else '(Public)')
			print('\tMessage:', msg['text'], '\n')
		else:
			print('Message:', contentType, chatType, chatId, '(' + userInfo['first_name'], userInfo['last_name'] + ')')
			return

		origText = msg['text'].replace('@SamTheNerdBot', '')
		origText = origText[1:] if origText[0] == '/' else origText
		text = origText.lower()

		# Admin Commands
		if userInfo['id'] == glob.ADMIN_ID:
			if text == 'reboot':
				if len(sys.argv) >= 2:
					sys.argv = sys.argv[:1]
				else:
					await m(chatId, 'Rebooting...')
					os.execv(sys.executable, ['python3'] + sys.argv[:1] + [str(chatId)])
			elif text.startswith('git '):
				await m(chatId, processOutput(text))
			elif text == 'update' or text == 'refresh' or text == 'reload':
				await m(chatId, 'Refreshing Response List...')
				loadReplies()
				await m(chatId, 'Done!')
			elif text.startswith('python'):
				cmd = text[6:]
				try:
					await m(chatId, eval(cmd))
				except:
					await m(chatId, 'Error parsing Python code.')

		await m(chatId, getReply(chatId, origText, userInfo))
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
