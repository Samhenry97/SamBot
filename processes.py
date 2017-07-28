import pymysql, pyttsx3
import threading, asyncio, requests, time
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
						await bot.sendMessage(a['chatId'], 'Alarm for ' + user['nickName'] + '!!')
					else:
						message = a['message']
						print('Sending Reminder to ' + user['firstName'] + ': ' + message)
						await bot.sendMessage(a['chatId'], 'Reminder for ' + user['nickName'] + ': ' + message)
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
		except KeyboardInterrupt:
			print('Tech Writing Keep Alive Shutting Down...')
			break

def speechEngine(engine):
	while True:
		try:
			engine.runAndWait()
		except KeyboardInterrupt:
			print('Speech Engine Shutting Down...')
			break