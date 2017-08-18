import os, sys, random, asyncio
import telepot.aio, pyowm, pyaudio
import database, reply, hotword, bots.messenger, bots.telegram, bots.sms, bots.kik
from fbchat.models import *
from util import Loader

OWM_TOKEN = os.environ['OWM_TOKEN']
ADMIN_IDS = [int(x) for x in os.environ['ADMIN_IDS'].split(',')]
ESPEAK_OPTIONS = ['espeak', '-ven-us+f3', '-s170']
PLATFORMS = { 'm': 'Messenger', 't': 'Telegram', 's': 'SMS', 'k': 'Kik' }
pause = False
db = owm = speech = None
users = {}
chats = {}
speechQueue = []

def init():
	global db, owm, users, chat, chatUsers, speech
	
	print('\n' + '-' * 50)
	print('Initializing in Production Mode...')
	print('-' * 50)
	
	with Loader('Telegram Bot'):
		bots.telegram.init()
	with Loader('Messenger Bot'):
		bots.messenger.init()
	with Loader('Kik Bot'):
		bots.kik.init()
	with Loader('Twilio Bot'):
		bots.sms.init()
	with Loader('Database'):
		db = database.Database()
		db.loadUsers(users)
		db.loadChats(chats)
	with Loader('OWM (Weather)'):
		owm = pyowm.OWM(OWM_TOKEN)
	with Loader('Microphone'):
		hotword.init()
		
	print('\n' + '-' * 50)
	print('Initialization Complete!')
	print('-' * 50)

async def m(chat, text): # ASync Message
	if chat['type'] == 't':
		await bots.telegram.client.sendMessage(chat['chatId'], text)
	else:
		bm(chat, text)
		
def bm(chat, text): # Block Message
	if chat['type'] == 't':
		bots.telegram.bclient.sendMessage(chat['chatId'], text)
	elif chat['type'] == 'm':
		bots.messenger.sendMessage(text, str(chat['chatId']), [ThreadType.USER, ThreadType.GROUP][chat['public']])
	elif chat['type'] == 's':
		bots.sms.sendMessage(chat['chatId'], text)
	elif chat['type'] == 'k':
		recipient = db.getUserForPrivateChat(chat['id'])
		bots.kik.sendMessage(recipient['userName'], chat['uuid'], text)
		
def sendPhoto(chat, name, web):
	if web:
		if chat['type'] == 't':
			bots.telegram.bclient.sendPhoto(chat['chatId'], name)
		elif chat['type'] == 'm':
			bots.messenger.client.sendRemoteImage(name, thread_id=chat['chatId'], thread_type=[ThreadType.USER, ThreadType.GROUP][chat['public']])
	else:
		if chat['type'] == 't':
			bots.telegram.bclient.sendPhoto(chat['chatId'], open(name, 'rb'))
		elif chat['type'] == 'm':
			bots.messenger.client.sendLocalImage(name, thread_id=chat['chatId'], thread_type=[ThreadType.USER, ThreadType.GROUP][chat['public']])
		
		
def changeNickname(newName, chat, userInfo):
	if userInfo['type'] == 'm':
		bots.messenger.client.changeNickname(newName, str(userInfo['userId']), thread_id=str(chat['chatId']), thread_type=[ThreadType.USER, ThreadType.GROUP][chat['public']])
	db.setNickname(userInfo['id'], newName)
	
def messageAdmins(text):
	for id in ADMIN_IDS:
		if db.getUserById(id)['type'] != 's': # Don't send text because charges
			chat = db.getPrivateChatForUser(id)
			bm(chat, text)

def say(message):
	global speechQueue
	speechQueue.append(message)

def cleanup():
	global db
	db.close()
