import pymysql, pyttsx3
import threading, asyncio, requests, time
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
					user = alarmDB.getUser(a['userId'])
					if a['message'] == None:
						print('Sending Alarm to ' + user['firstName'] + '.')
						await glob.m(a['chatId'], 'Alarm for ' + user['nickName'] + '!!')
					else:
						message = a['message']
						print('Sending Reminder to ' + user['firstName'] + ': ' + message)
						await glob.m(a['chatId'], 'Reminder for ' + user['nickName'] + ': ' + message)
					alarmDB.deleteAlarm(a['id'])
			alarmDB.close()
			await asyncio.sleep(1)
		except KeyboardInterrupt:
			print('Alarm Check Shutting Down...')
			break
		except pymysql.err.OperationalError:
			alarmDB.close()
			alarmDB.open()

def techWritingKeepAlive():
	while True:
		try:
			requests.get('http://bootableusb.herokuapp.com')
			time.sleep(1)
		except KeyboardInterrupt:
			print('Tech Writing Keep Alive Shutting Down...')
			break

def speechEngine(engine):
	while True:
		try:
			if len(glob.speechQueue) > 0:
				engine.say(glob.speechQueue[0])
				del glob.speechQueue[0]
				engine.runAndWait()
			else:
				time.sleep(1)
		except KeyboardInterrupt:
			print('Speech Engine Shutting Down...')
			break
			
async def manual():
	while True:
		s = await ainput()
		if s.startswith('message'):
			u = glob.db.getUsersByName(s.split()[1])
			msg = bytes(' '.join(s.split()[2:]), "utf-8").decode("unicode_escape")
			if len(u) == 1:
				chat = glob.db.getPrivateChat(u[0]['id'])
				await glob.m(chat['id'], msg)
				print('Sent Message.')
			elif len(u) == 0:
				print('Could not find user.')
			else:
				print('Which User? (select number)')
				for i in range(len(u)):
					print('(%d) %s %s' % (i, u[i]['firstName'], u[i]['lastName']))
				ans = int(input())
				if ans >= 0 and ans < len(u):
					chat = glob.db.getPrivateChat(u[ans]['id'])
					await glob.m(chat['id'], msg)
					print('Sent Message.')
				else:
					print('Please enter a correct user.')
