import os, logging, random
import pymysql
import util, glob, reply
from fbchat import log, Client
from fbchat.models import *

client = None
colors = ['BILOBA_FLOWER', 'BRILLIANT_ROSE', 'CAMEO', 'DEEP_SKY_BLUE', 'FERN', 
		  'FREE_SPEECH_GREEN', 'GOLDEN_POPPY', 'LIGHT_CORAL', 'MEDIUM_SLATE_BLUE', 
		  'MESSENGER_BLUE', 'PICTON_BLUE', 'PUMPKIN', 'RADICAL_RED', 'SHOCKING', 'VIKING']


class MessengerSamBot(Client):
	def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
		try:
			db = glob.db
			
			self.markAsDelivered(author_id, thread_id)
			self.markAsRead(author_id)
			self.setTypingStatus(TypingStatus.TYPING, thread_id=thread_id)
			
			if author_id == self.uid:
				return
			
			userId = int(author_id)
			chatId = int(thread_id)
			user = db.getUser(userId, 'm')
			if user:
				info = { 'id': userId, 'first_name': user['firstName'], 'last_name': user['lastName'], 'username': user['userName'] }
			else:
				user = self.fetchUserInfo(author_id)[author_id]
				info = { 'id': userId, 'first_name': user.name.split()[0], 'last_name': ' '.join(user.name.split()[1:]), 'username': ''.join(user.name.split()) }
				
			userInfo, chat = util.checkDatabase(info, chatId, thread_type == ThreadType.GROUP, 'm')
			
			print('Facebook message from', userInfo['firstName'], userInfo['lastName'])
			print('\tChat ID:', chatId, '(Public)' if thread_type == ThreadType.GROUP else '(Private)')
			print('\tMessage:', message, '\n')
			
			if message.lower().startswith('color'):
				self.changeThreadColor(eval('ThreadColor.' + random.choice(colors)), thread_id=thread_id)
				return
			
			response = reply.getReply(message, userInfo, chat)
			if response.strip():
				self.sendMessage(response, thread_id=thread_id, thread_type=thread_type)
		except (ConnectionAbortedError, pymysql.err.OperationalError, pymysql.err.InterfaceError):
			self.sendMessage('Connection lost to the database. Connecting...', thread_id=thread_id, thread_type=thread_type)
			db.close()
			db.open()
			self.sendMessage('Connected!', thread_id=thread_id, thread_type=thread_type)
		except Exception as e:
			glob.messageAdmins('Uncaught Error: {}'.format(e))
			self.sendMessage('Sorry, something went wrong... ', thread_id=thread_id, thread_type=thread_type)
			
def sendMessage(text, chatId, chatType):
	client.sendMessage(text, thread_id=chatId, thread_type=chatType)

def init():
	global client
	log.setLevel(logging.ERROR)
	client = MessengerSamBot(os.environ['BOT_EMAIL'], os.environ['BOT_PASS'])

def listen():
	client.listen()
