import os, logging
import util, glob
from reply import getReply
from fbchat import log, Client
from fbchat.models import *

client = None

##################################################################################################
##################################################################################################

class FacebookSamBot(Client):
	def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
		self.markAsDelivered(author_id, thread_id)
		self.markAsRead(author_id)
		self.setTypingStatus(TypingStatus.TYPING, thread_id=thread_id)
		
		if author_id == self.uid:
			return
		
		userId = int(author_id)
		chatId = int(thread_id)
		user = glob.db.getUser(userId, 'm')
		if user:
			info = { 'id': userId, 'first_name': user['firstName'], 'last_name': user['lastName'], 'username': user['userName'] }
		else:
			self.changeThreadColor(ThreadColor.MESSENGER_ORANGE, thread_id=thread_id)
			user = self.fetchUserInfo(author_id)[author_id]
			info = { 'id': userId, 'first_name': user.name.split()[0], 'last_name': ' '.join(user.name.split()[1:]), 'username': ''.join(user.name.split()) }
			
		userInfo = util.checkDatabase(info, chatId, thread_type == ThreadType.GROUP, 'm')
		
		print('Facebook message from', userInfo['firstName'], userInfo['lastName'])
		print('\tChat ID:', chatId, '(Public)' if thread_type == ThreadType.GROUP else '(Private)')
		print('\tMessage:', message, '\n')
		
		response = getReply(chatId, message, userInfo)
		if response.strip():
			self.sendMessage(response, thread_id=thread_id, thread_type=thread_type)

def init():
	global client
	log.setLevel(logging.ERROR)
	client = FacebookSamBot(os.environ['BOT_EMAIL'], os.environ['BOT_PASS'])

def listen():
	global client
	client.listen()
