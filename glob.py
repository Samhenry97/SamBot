import os, sys, random, asyncio, requests, io
import telepot.aio, pyowm, pyaudio
import database, reply, hotword, bots.messenger, bots.telegram, bots.sms, bots.kik, bots.whatsapp, bots.disc
from fbchat.models import *
from util import Loader

OWM_TOKEN = os.environ['OWM_TOKEN']
WEBHOOK = os.environ['WEBHOOK']
ESPEAK_OPTIONS = ['espeak', '-ven-us+m3', '-s170']
PLATFORMS = { 'm': 'Messenger', 't': 'Telegram', 's': 'SMS', 'k': 'Kik', 'w': 'WhatsApp', 'o': 'Online', 'd': 'Discord' }
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
	#with Loader('Messenger Bot'):
	#	bots.messenger.init()
	with Loader('Kik Bot'):
		bots.kik.init()
	with Loader('Twilio Bot'):
		bots.sms.init()
	with Loader('WhatsApp Bot'):
		bots.whatsapp.init()
	with Loader('Discord Bot'):
		bots.disc.init()
	with Loader('OWM (Weather)'):
		owm = pyowm.OWM(OWM_TOKEN)
	with Loader('Database'):
		db = database.Database()
		db.loadUsers(users)
		db.loadChats(chats)
		reply.loadReplies()
	with Loader('Microphone'):
		hotword.init()
		
	print('\n' + '-' * 50)
	print('Initialization Complete!')
	print('-' * 50)

async def m(chat, text): # Async Message
	if chat['type'] == 't':
		await bots.telegram.client.sendMessage(chat['chatId'], text)
	elif chat['type'] == 'd':
		await bots.disc.sendMessage(chat['chatId'], text)
	else:
		bm(chat, text)
		
def bm(chat, text): # Block Message
	if chat['type'] == 't':
		bots.telegram.bclient.sendMessage(chat['chatId'], text)
	#elif chat['type'] == 'm':
	#	bots.messenger.sendMessage(text, str(chat['chatId']), [ThreadType.USER, ThreadType.GROUP][chat['public']])
	elif chat['type'] == 's':
		bots.sms.sendMessage(chat['chatId'], text)
	elif chat['type'] == 'k':
		recipient = db.getUserForChat(chat['id'])
		bots.kik.sendMessage(recipient['userName'], chat['uuid'], text)
	elif chat['type'] == 'w':
		bots.whatsapp.sendMessage(chat['uuid'], text)
	elif chat['type'] == 'd':
		loop = asyncio.get_event_loop()
		loop.create_task(bots.disc.sendMessage(chat['chatId'], text))
		
def sendPhoto(chat, name, web=True):
	if web:
		if chat['type'] == 't':
			bots.telegram.bclient.sendPhoto(chat['chatId'], name)
		elif chat['type'] == 'm':
			bots.messenger.client.sendRemoteImage(name, thread_id=chat['chatId'], thread_type=[ThreadType.USER, ThreadType.GROUP][chat['public']])
		elif chat['type'] == 'k':
			recipient = db.getUserForPrivateChat(chat['id'])
			bots.kik.sendPhoto(recipient['userName'], chat['uuid'], name)
		elif chat['type'] == 's':
			bots.sms.sendPhoto(chat['chatId'], name)
		elif chat['type'] == 'd':
			loop = asyncio.get_event_loop()
			loop.create_task(bots.disc.sendPhoto(chat['chatId'], name))
	else:
		if chat['type'] == 't':
			bots.telegram.bclient.sendPhoto(chat['chatId'], open(name, 'rb'))
		elif chat['type'] == 'm':
			bots.messenger.client.sendLocalImage(name, thread_id=chat['chatId'], thread_type=[ThreadType.USER, ThreadType.GROUP][chat['public']])
		
		
def changeNickname(newName, chat, userInfo):
	if userInfo['type'] == 'm':
		bots.messenger.client.changeNickname(newName, str(userInfo['userId']), thread_id=str(chat['chatId']), thread_type=[ThreadType.USER, ThreadType.GROUP][chat['public']])
	elif userInfo['type'] == 'd':
		loop = asyncio.get_event_loop()
		loop.create_task(bots.disc.changeNickname(newName, chat, userInfo))
	db.setNickname(userInfo['id'], newName)
	
def messageAdmins(text):
	for user in db.getAdmins():
		if user['type'] not in ['s', 'o']: # Don't send text because charges
			chat = db.getPrivateChatForUser(user['id'])
			bm(chat, text)

def say(message):
	global speechQueue
	speechQueue.append(message)

def cleanup():
	global db
	db.close()
