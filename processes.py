import threading, asyncio, requests, time, subprocess
import pymysql, reply, bots.sms
import glob
from aioconsole import ainput
from util import getDate
from database import Database

async def alarmCheck():
	while True:
		try:
			db = glob.db
			alarms = db.getAlerts()
			for a in alarms:
				user = db.getUserById(a['userId'])
				if a['message'] == None:
					print('[Sending Alarm to {}]\n'.format(user['firstName']))
					message = 'Alarm for {}!'.format(user['nickName'] or user['firstName'])
				else:
					print('[Sending Reminder to {}: {}]\n'.format(user['firstName'], a['message']))
					message = 'Reminder for {}: {}'.format(user['nickName'] or user['firstName'], a['message'])
				if user['type'] == 'o':
					db.addMessage(user['id'], message, False)
					if user['userId']:
						bots.sms.sendMessage(user['userId'], message)
				else:
					await glob.m(db.getChatById(a['chatId']), message)
				db.deleteAlarm(a['id'])
			await asyncio.sleep(1)
		except (ConnectionAbortedError, pymysql.err.OperationalError, pymysql.err.InterfaceError):
			db.close()
			db.open()
		except Exception as e:
			glob.messageAdmins('Uncaught Error in Alarm Check: {}'.format(e))

def keepAlive():
	while True:
		requests.get('http://bootableusb.herokuapp.com')
		requests.get('http://unicoders.herokuapp.com')
		time.sleep(30)

def speechEngine(engine):
	while True:
		if len(glob.speechQueue) > 0:
			glob.pause = True
			subprocess.call(glob.ESPEAK_OPTIONS + [glob.speechQueue[0]])
			del glob.speechQueue[0]
			glob.pause = False
		else:
			time.sleep(1)
			
async def manual():
	db = glob.db
	while True:
		try:
			s = await ainput()
			userInfo = glob.db.getAdmins()[0]
			chat = glob.db.getPrivateChatForUser(userInfo['id'])
			
			if s.startswith('message'):
				u = db.getUsersByName(s.split()[1])
				msg = bytes(' '.join(s.split()[2:]), "utf-8").decode("unicode_escape")
				if len(u) == 1:
					await glob.m(glob.db.getPrivateChatForUser(u[0]['id']), msg)
					print('Sent Message.')
				elif len(u) == 0:
					print('Could not find user.')
				else:
					print('Which User? (select number)')
					for i in range(len(u)):
						print('(%d) %s %s [%s]' % (i, u[i]['firstName'], u[i]['lastName'], glob.PLATFORMS[u[i]['type']]))
					ans = int(await ainput())
					if ans >= 0 and ans < len(u):
						await glob.m(db.getPrivateChatForUser(u[ans]['id']), msg)
						print('Sent Message.')
					else:
						print('Please enter a correct user.')
			else:
				response = reply.getReply(s, userInfo, chat)
				if response.strip():
					glob.say(response)
					print(response)
				else:
					glob.say('Sorry, I didn\'t get that.')
					print('Sorry, I didn\'t get that.')
		except (ConnectionAbortedError, pymysql.err.OperationalError, pymysql.err.InterfaceError):
			print('Connection lost to the database. Connecting...')
			db.close()
			db.open()
			print('Connected!')	
		except Exception as e:
			print('Could not send message:', e)
