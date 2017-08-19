import threading, asyncio, requests, time, subprocess
import pymysql, reply, bots.sms
import glob
from aioconsole import ainput
from util import getDate
from database import Database

async def alarmCheck():
	db = Database()
	while True:
		try:
			db.open()
			alarms = db.getAlerts()
			for a in alarms:
				if a['time'] < getDate():
					message = 'Alarm'
					user = db.getUserById(a['userId'])
					if a['message'] == None:
						print('[Sending Alarm to ' + user['firstName'] + '.]\n')
						await glob.m(db.getChatById(a['chatId']), 'Alarm for ' + (user['nickName'] or user['firstName']) + '!')
					else:
						message = a['message']
						print('[Sending Reminder to ' + user['firstName'] + ': ' + message, ']\n')
						await glob.m(db.getChatById(a['chatId']), 'Reminder for ' + (user['nickName'] or user['firstName']) + ': ' + message)
					db.deleteAlarm(a['id'])
			db.close()
			await asyncio.sleep(1)
		except pymysql.err.OperationalError:
			db.close()
			db.open()

def techWritingKeepAlive():
	while True:
		requests.get('http://bootableusb.herokuapp.com')
		time.sleep(20)

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
			userInfo = db.getUserById(glob.ADMIN_IDS[0])
			chat = db.getChat(131453030, userInfo['type'])
			
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
			elif s.startswith('text'):
				number = s.split()[1]
				msg = ' '.join(s.split()[2:])
				bots.sms.sendMessage('1' + number, msg)
				print('Sent Text.')
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
