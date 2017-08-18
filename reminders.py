import re
import util, glob
from datetime import datetime, timedelta

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

def tryParse(chat, text, origText, userInfo, genReply):
	db = glob.db

	mat = remindStart.match(text)
	if mat:
		text = mat.group('command')
		for regex in remindToRegex:
			r = regex.match(text)
			if r:
				msg = r.group('message')
				date = util.dateFromNow(r.group('amount'), r.group('units'))
				db.addReminder(userInfo['id'], chat['id'], msg, date)
				return genReply('reminder', userInfo, util.convertDate(date))
		for regex in remindAtRegex:
			r = regex.match(text)
			if r:
				msg = r.group('message')
				date = util.dateWithOffset(r.group('h'), r.group('m'), r.group('s'), r.group('ampm'), r.group('timeofday'), r.group('offset'))
				db.addReminder(userInfo['id'], chat['id'], msg, date)
				return genReply('reminder', userInfo, util.convertDate(date))
		return genReply('reminderhelp', userInfo)

	mat = alarmStart.match(text)
	if mat:
		text = mat.group('command')
		r = alarmRegex.match(text)
		if r:
			date = util.dateFromNow(r.group('amount'), r.group('units'))
			db.addAlarm(userInfo['id'], chat['id'], date)
			return genReply('alarm', userInfo, util.convertDate(date))
		for regex in alarmAtRegex:
			r = regex.match(text)
			if r:
				date = util.dateWithOffset(r.group('h'), r.group('m'), r.group('s'), r.group('ampm'), r.group('timeofday'), r.group('offset'))
				db.addAlarm(userInfo['id'], chat['id'], date)
				return genReply('alarm', userInfo, util.convertDate(date))
		return genReply('reminderhelp', userInfo)

	if text.startswith('clear alarms') or text.startswith('clearalarms'):
		if 'all' in text:
			db.clearAlarms(userInfo['id'])
			return userInfo['firstName'] + ', all your alarms are cleared.'
		else:
			db.clearAlarms(userInfo['id'], chat['id'])
			return userInfo['firstName'] + ', your alarms for this chat are cleared.'
	elif text.startswith('clear reminders') or text.startswith('clearreminders'):
		if 'all' in text:
			db.clearReminders(userInfo['id'])
			return userInfo['firstName'] + ', all your reminders are cleared.'
		else:
			db.clearReminders(userInfo['id'], chat['id'])
			return userInfo['firstName'] + ', your reminders for this chat are cleared.'
	elif text.startswith('list alarms'):
		ans = []
		if 'all' in text:
			alarms = db.getAlarms(userId=userInfo['id'])
			if len(alarms) == 0:
				ans.append('No alarms set for ' + userInfo['firstName'] + '.')
			else:
				ans.append('All alarms for ' + userInfo['firstName'] + ':')
		elif 'chat' in text:
			alarms = db.getAlarms(chatId=chat['id'])
			if len(alarms) == 0:
				ans.append('No alarms in this chat.')
			else:
				ans.append('All alarms in this chat: ')
		else:
			alarms = db.getAlarms(userInfo['id'], chat['id'])
			if len(alarms) == 0:
				ans.append('No alarms in this chat for ' + userInfo['firstName'] + '.')
			else:
				ans.append('Alarms in this chat for ' + userInfo['firstName'] + ':')
		
		for a in alarms:
			ans.append(util.convertDate(a['time']))
		return '\n'.join(ans)
	elif text.startswith('list reminders'):
		ans = []
		if 'all' in text:
			reminders = db.getReminders(userId=userInfo['id'])
			if len(reminders) == 0:
				ans.append('No reminders set for ' + userInfo['firstName'] + '.')
			else:
				ans.append('All reminders for ' + userInfo['firstName'] + ':')
		elif 'chat' in text:
			reminders = db.getReminders(chatId=chat['id'])
			if len(reminders) == 0:
				ans.append('No reminders in this chat.')
			else:
				ans.append('All reminders in this chat: ')
		else:
			reminders = db.getReminders(userInfo['id'], chat['id'])
			if len(reminders) == 0:
				ans.append('No reminders in this chat for ' + userInfo['firstName'] + '.')
			else:
				ans.append('Reminders in this chat for ' + userInfo['firstName'] + ':')
		
		for r in reminders:
			ans.append('@ ' + util.convertDate(r['time']) + ': ' + r['message'])
		return '\n'.join(ans)
	return ''
