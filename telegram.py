import os, sys, time, random, hashlib, subprocess, re
import util, glob
import telepot, pymysql

from glob import m
from reply import getReply, tests, loadReplies
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

		addUser(userInfo, chatId)
		
		if contentType == 'text':
			print('Telegram message from', userInfo['first_name'], userInfo['last_name'])
			print('\tChat ID:', chatId, '(Private)' if chatId >= 0 else '(Public)')
			print('\tMessage:', msg['text'], '\n')
		else:
			print('Message:', contentType, chatType, chatId, '(' + userInfo['first_name'], userInfo['last_name'] + ')')
			return

		origText = msg['text'].replace('@SamTheNerdBot', '')
		origText = origText[1:] if origText[0] == '/' else origText
		
		response = getReply(chatId, origText, userInfo)
		if response.strip():
			await m(chatId, response)
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
