import pymysql
import threading, asyncio, requests, time, subprocess
import glob
from aioconsole import ainput
from util import getDate
from database import Database

async def alarmCheck(bot):
	alarmDB = Database()
	while True:
		try:
			alarmDB.open()
			alarms = alarmDB.getAlerts()
			for a in alarms:
				if a['time'] < getDate():
					message = 'Alarm'
					user = alarmDB.getUserById(a['userId'])
					if a['message'] == None:
						print('Sending Alarm to ' + user['firstName'] + '.')
						await glob.m(alarmDB.getChatById(a['chatId']), 'Alarm for ' + user['nickName'] + '!', user['type'])
					else:
						message = a['message']
						print('Sending Reminder to ' + user['firstName'] + ': ' + message)
						await glob.m(alarmDB.getChatById(a['chatId']), 'Reminder for ' + user['nickName'] + ': ' + message, user['type'])
					alarmDB.deleteAlarm(a['id'])
			alarmDB.close()
			await asyncio.sleep(1)
		except pymysql.err.OperationalError:
			alarmDB.close()
			alarmDB.open()

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
	while True:
		try:
			s = await ainput()
			if s.startswith('message'):
				u = glob.db.getUsersByName(s.split()[1])
				msg = bytes(' '.join(s.split()[2:]), "utf-8").decode("unicode_escape")
				if len(u) == 1:
					await glob.m(u[0]['id'], msg)
					print('Sent Message.')
				elif len(u) == 0:
					print('Could not find user.')
				else:
					print('Which User? (select number)')
					for i in range(len(u)):
						print('(%d) %s %s' % (i, u[i]['firstName'], u[i]['lastName']))
					ans = int(await ainput())
					if ans >= 0 and ans < len(u):
						await glob.m(u[ans]['id'], msg)
						print('Sent Message.')
					else:
						print('Please enter a correct user.')
		except Exception as e:
			print('Could not send message: ' + str(e))
