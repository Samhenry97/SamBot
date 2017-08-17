import os, sys, random, asyncio, logging, flask
import telepot.aio, pyowm, pyaudio
import database, reply, hotword, facebook, telegram, sms, kikbot
from fbchat.models import *

OWM_TOKEN = os.environ['OWM_TOKEN']
ADMIN_IDS = [int(x) for x in os.environ['ADMIN_IDS'].split(',')]
ESPEAK_OPTIONS = ['espeak', '-ven-us+f3', '-s170']
PLATFORMS = { 'm': 'Messenger', 't': 'Telegram', 's': 'SMS', 'k': 'Kik' }
pause = False
db = owm = speech = None
users = {}
chats = {}
speechQueue = []

server = flask.Flask(__name__) # For SMS and Kik
@server.route('/sms', methods=['GET', 'POST'])
def smsMessage():
	return sms.onMessage()
	
@server.route('/kik', methods=['GET', 'POST'])
def kikMessage():
	return kikbot.onMessage()

def init():
	if len(sys.argv) < 2 or sys.argv[1] != 'DEBUG':
		logging.basicConfig(level=logging.ERROR)
		logging.getLogger().setLevel(logging.ERROR)
	
	global db, owm, users, chat, chatUsers, speech
	print('\n' + '-' * 50)
	print('Initializing in Production Mode...')
	print('-' * 50)
	print('Loading Telegram Bot...')
	telegram.init()
	print('Done!\n')
	print('Loading Facebook Bot...')
	facebook.init()
	print('Done!\n')
	print('Loading Kik Bot...')
	kikbot.init()
	print('Done!\n')
	print('Loading Twilio...')
	sms.init()
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

async def m(chat, text):
	if chat['type'] == 't':
		await telegram.bot.sendMessage(chat['chatId'], text)
	else:
		bm(chat, text)
		
def bm(chat, text):
	if chat['type'] == 't':
		telegram.bbot.sendMessage(chat['chatId'], text)
	elif chat['type'] == 'm':
		facebook.client.sendMessage(text, thread_id=str(chat['chatId']), thread_type=[ThreadType.USER, ThreadType.GROUP][chat['public']])
	elif chat['type'] == 's':
		sms.message(chat['chatId'], text)
	elif chat['type'] == 'k':
		recipient = db.getUserForPrivateChat(chat['id'])
		kikbot.sendMessage(recipient['userName'], chat['uuid'], text)
		
def sendPhoto(chat, name, web):
	if web:
		if chat['type'] == 't':
			telegram.bbot.sendPhoto(chat['chatId'], name)
		elif chat['type'] == 'm':
			facebook.client.sendRemoteImage(name, thread_id=chat['chatId'], thread_type=[ThreadType.USER, ThreadType.GROUP][chat['public']])
	else:
		if chat['type'] == 't':
			telegram.bbot.sendPhoto(chat['chatId'], open(name, 'rb'))
		elif chat['type'] == 'm':
			facebook.client.sendLocalImage(name, thread_id=chat['chatId'], thread_type=[ThreadType.USER, ThreadType.GROUP][chat['public']])
		
		
def changeNickname(newName, chat, userInfo):
	if userInfo['type'] == 'm':
		facebook.client.changeNickname(newName, str(userInfo['userId']), thread_id=str(chat['chatId']), thread_type=[ThreadType.USER, ThreadType.GROUP][chat['public']])
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
