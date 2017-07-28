import util, glob
import re
from datetime import datetime, timedelta
from reply import genReply
from glob import message, m

remindStart = re.compile('((remind( *me)?)|(set a reminder))(?P<command>.+)')
remindToRegex = [
	re.compile('( *to)?(?P<message>.+)in *(?P<amount>([0-9]+)|((zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|trillion|a few)( |-)*)+) *(?P<units>seconds?|minutes?|hours?|days?|weeks?|months?|years?) *$'),
	re.compile(' *in *(?P<amount>([0-9]+)|((zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|trillion|a few)( |-)*)+) *(?P<units>seconds?|minutes?|hours?|days?|weeks?|months?|years?) *to *(?P<message>.+) *$')
]

remindAtRegex = [
	re.compile(' *(?P<offset>today|tomorrow|next week|next month|next year) *(at|for) *(((?P<h>[0-9][0-9]?)(:(?P<m>[0-9][0-9]))?(:(?P<s>[0-9][0-9]))? *(?P<ampm>am|pm)?)|(?P<timeofday>noon|afternoon|midnight|sunrise|sunset|dawn|dusk)) *to(?P<message>.+)'),
	re.compile(' *(at|for) *(((?P<h>[0-9][0-9]?)(:(?P<m>[0-9][0-9]))?(:(?P<s>[0-9][0-9]))? *(?P<ampm>am|pm)?)|(?P<timeofday>noon|afternoon|midnight|sunrise|sunset|dawn|dusk)) *(?P<offset>today|tomorrow|next week|next month|next year) *to(?P<message>.+)'),
	re.compile(' *(at|for) *(((?P<h>[0-9][0-9]?)(:(?P<m>[0-9][0-9]))?(:(?P<s>[0-9][0-9]))? *(?P<ampm>am|pm)?)|(?P<timeofday>noon|afternoon|midnight|sunrise|sunset|dawn|dusk)) *to(?P<message>.+)(?P<offset>chicken)?'),
	re.compile('( *to)(?P<message>.+)(?P<offset>today|tomorrow|next week|next month|next year) *(at|for) *(((?P<h>[0-9][0-9]?)(:(?P<m>[0-9][0-9]))?(:(?P<s>[0-9][0-9]))? *(?P<ampm>am|pm)?)|(?P<timeofday>noon|afternoon|midnight|sunrise|sunset|dawn|dusk))'),
	re.compile('( *to)(?P<message>.+) *(at|for) *(((?P<h>[0-9][0-9]?)(:(?P<m>[0-9][0-9]))?(:(?P<s>[0-9][0-9]))? *(?P<ampm>am|pm)?)|(?P<timeofday>noon|afternoon|midnight|sunrise|sunset|dawn|dusk)) *(?P<offset>today|tomorrow|next week|next month|next year)'),
	re.compile('( *to)(?P<message>.+) *(at|for) *(((?P<h>[0-9][0-9]?)(:(?P<m>[0-9][0-9]))?(:(?P<s>[0-9][0-9]))? *(?P<ampm>am|pm)?)|(?P<timeofday>noon|afternoon|midnight|sunrise|sunset|dawn|dusk))(?P<offset>chicken)?')
]

alarmStart = re.compile('((alarm )|(set an alarm ))(?P<command>.+)')
alarmRegex = re.compile(' *in *(?P<amount>([0-9]+)|((zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|trillion|a few)( |-)*)+) *(?P<units>seconds?|minutes?|hours?|days?|weeks?|months?|years?)')
alarmAtRegex = [
	re.compile(' *(?P<offset>today|tomorrow|next week|next month|next year) *(at|for) *(((?P<h>[0-9][0-9]?)(:(?P<m>[0-9][0-9]))?(:(?P<s>[0-9][0-9]))? *(?P<ampm>am|pm)?)|(?P<timeofday>noon|afternoon|midnight|sunrise|sunset|dawn|dusk))'),
	re.compile(' *(at|for) *(((?P<h>[0-9][0-9]?)(:(?P<m>[0-9][0-9]))?(:(?P<s>[0-9][0-9]))? *(?P<ampm>am|pm)?)|(?P<timeofday>noon|afternoon|midnight|sunrise|sunset|dawn|dusk)) *(?P<offset>today|tomorrow|next week|next month|next year)'),
	re.compile(' *(at|for) *(((?P<h>[0-9][0-9]?)(:(?P<m>[0-9][0-9]))?(:(?P<s>[0-9][0-9]))? *(?P<ampm>am|pm)?)|(?P<timeofday>noon|afternoon|midnight|sunrise|sunset|dawn|dusk))(?P<offset>chicken)?')
]

async def tryParse(text, origText, chatId, userInfo):
	bot = glob.bot
	db = glob.db

	mat = remindStart.match(text)
	if mat:
		text = mat.group('command')
		for regex in remindToRegex:
			r = regex.match(text)
			if r:
				msg = r.group('message')
				date = util.dateFromNow(r.group('amount'), r.group('units'))
				db.addReminder(userInfo['id'], chatId, msg, date)
				await message(chatId, 'reminder', userInfo, str(date))
				return True
		for regex in remindAtRegex:
			r = regex.match(text)
			if r:
				msg = r.group('message')
				date = util.dateWithOffset(r.group('h'), r.group('m'), r.group('s'), r.group('ampm'), r.group('timeofday'), r.group('offset'))
				db.addReminder(userInfo['id'], chatId, msg, date)
				await message(chatId, 'reminder', userInfo, str(date))
				return True
		await message(chatId, 'noreminder', userInfo)
		await message(chatId, 'reminderhelp', userInfo)
		return False

	mat = alarmStart.match(text)
	if mat:
		text = mat.group('command')
		r = alarmRegex.match(text)
		if r:
			date = util.dateFromNow(r.group('amount'), r.group('units'))
			db.addAlarm(userInfo['id'], chatId, date)
			await message(chatId, 'alarm', userInfo, str(date))
			return True
		for regex in alarmAtRegex:
			r = regex.match(text)
			if r:
				date = util.dateWithOffset(r.group('h'), r.group('m'), r.group('s'), r.group('ampm'), r.group('timeofday'), r.group('offset'))
				db.addAlarm(userInfo['id'], chatId, date)
				await message(chatId, 'alarm', userInfo, str(date))
				return True
		await message(chatId, 'noreminder', userInfo)
		await message(chatId, 'reminderhelp', userInfo)
		return False

	if text.startswith('clear alarms') or text.startswith('clearalarms'):
		if 'all' in text:
			db.clearAlarms(userInfo['id'])
			await m(chatId, userInfo['first_name'] + ', all your alarms are cleared.')
		else:
			db.clearAlarms(userInfo['id'], chatId)
			await m(chatId, userInfo['first_name'] + ', your alarms for this chat are cleared.')
	elif text.startswith('clear reminders') or text.startswith('clearreminders'):
		if 'all' in text:
			db.clearReminders(userInfo['id'])
			await m(chatId, userInfo['first_name'] + ', all your reminders are cleared.')
		else:
			db.clearReminders(userInfo['id'], chatId)
			await m(chatId, userInfo['first_name'] + ', your reminders for this chat are cleared.')
	elif text.startswith('list alarms'):
		ans = []
		if 'all' in text:
			alarms = db.getAlarms(userId=userInfo['id'])
			if len(alarms) == 0:
				ans.append('No alarms set for ' + userInfo['first_name'] + '.')
			else:
				ans.append('All alarms for ' + userInfo['first_name'] + ':')
		elif 'chat' in text:
			alarms = db.getAlarms(chatId=chatId)
			if len(alarms) == 0:
				ans.append('No alarms in this chat.')
			else:
				ans.append('All alarms in this chat: ')
		else:
			alarms = db.getAlarms(userInfo['id'], chatId)
			if len(alarms) == 0:
				ans.append('No alarms in this chat for ' + userInfo['first_name'] + '.')
			else:
				ans.append('Alarms in this chat for ' + userInfo['first_name'] + ':')
		
		for a in alarms:
			ans.append('@' + str(a['time']))
		await m(chatId, '\n'.join(ans))
	elif text.startswith('list reminders'):
		ans = []
		if 'all' in text:
			reminders = db.getReminders(userId=userInfo['id'])
			if len(reminders) == 0:
				ans.append('No reminders set for ' + userInfo['first_name'] + '.')
			else:
				ans.append('All reminders for ' + userInfo['first_name'] + ':')
		elif 'chat' in text:
			reminders = db.getReminders(chatId=chatId)
			if len(reminders) == 0:
				ans.append('No reminders in this chat.')
			else:
				ans.append('All reminders in this chat: ')
		else:
			reminders = db.getReminders(userInfo['id'], chatId)
			if len(reminders) == 0:
				ans.append('No reminders in this chat for ' + userInfo['first_name'] + '.')
			else:
				ans.append('Reminders in this chat for ' + userInfo['first_name'] + ':')
		
		for r in reminders:
			ans.append('@ ' + str(r['time']) + ': ' + r['message'])
		await m(chatId, '\n'.join(ans))
	else:
		return False
	return True