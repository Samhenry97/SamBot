import re, random, requests, json, sys, os, subprocess, hashlib, time, geopy
import glob, reminders, util, bots.messenger, contest
from emoji import Emoji

replies = {}
tests = {}
replymap = {}

def loadReplies():
	inline = False
	inlineString = []
	key = ''
	with open('replies.sbot', 'r') as file:
		for line in file:
			line = line.strip('\n')
			if line == '' or line[0] == '#':
				continue
			elif inline:
				if line == '{end}':
					inline = False
					replies[key].append('\n'.join(inlineString))
					inlineString = []
				else:
					inlineString.append(line)
			elif line.startswith('key'):
				key = line.split()[1]
				replies[key] = []
			elif line.startswith('test'):
				words = line.split()[1:]
				tests[key] = len(words)
				for x in words:
					if x not in replymap:
						replymap[x] = { key: True }
					else:
						replymap[x][key] = True
			elif line == '{start}':
				inline = True
			else:
				replies[key].append(line)
				
def processOutput(command):
	p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	return out.decode('utf-8') + err.decode('utf-8')

def replaceWithVar(reply, name, value):
	def calcValue(m):
		nonlocal value
		x = int(m.group(2)) if m.group(2) else 1
		y = int(m.group(4)) if m.group(4) else x
		return value * random.randint(x, y)
	return re.sub('\{' + name + '\}(\(([0-9]+)(,([0-9]+))?\))?', calcValue, reply)

emojiRegex = re.compile('\{Emoji\.([^{]+)\}(\(([0-9]+)(,([0-9]+))?\))?')
argRegex = re.compile('\{arg\}(\(([0-9]+)(,([0-9]+))?\))?')
argNRegex = re.compile('\{arg([0-9]+)\}(\(([0-9]+)(,([0-9]+))?\))?')
wordRegex = re.compile('\{([^\{]+)\}(\(([0-9]+)(,([0-9]+))?\))?')
def genReply(replyType, info, *args):
	reply = random.choice(replies[replyType])

	reply = replaceWithVar(reply, 'fName', info['firstName'])
	reply = replaceWithVar(reply, 'lName', info['lastName'])
	reply = replaceWithVar(reply, 'uName', info['userName'])
	reply = replaceWithVar(reply, 'nName', info['nickName'] if info['nickName'].strip() else info['firstName'])

	def emoji(m):
		x = int(m.group(3)) if m.group(3) else 1
		y = int(m.group(5)) if m.group(5) else x
		return Emoji.get(m.group(1), x, y)
	reply = emojiRegex.sub(emoji, reply)

	argIndex = -1
	def nextArg(m):
		nonlocal argIndex
		argIndex += 1
		x = int(m.group(2)) if m.group(2) else 1
		y = int(m.group(4)) if m.group(4) else x
		return args[argIndex] * random.randint(x, y)
	reply = argRegex.sub(nextArg, reply)

	def argn(m):
		x = int(m.group(3)) if m.group(3) else 1
		y = int(m.group(5)) if m.group(5) else x
		return args[int(m.group(1)) - 1] * random.randint(x, y)
	reply = argNRegex.sub(argn, reply)

	def word(m):
		x = int(m.group(3)) if m.group(3) else 1
		y = int(m.group(5)) if m.group(5) else x
		return m.group(1) * random.randint(x, y)
	reply = wordRegex.sub(word, reply)

	return reply
	
	
	
def getReply(origText, userInfo, chat):
	db = glob.db
	text = origText.lower().strip()
	
	
	if text == '!talk':
		if chat['quiet'] == 0:
			return 'I\'m already talking'
		db.setQuiet(chat['id'], 0)
		return 'Yay! I can talk again!'
	elif text == '!direct':
		if chat['quiet'] == 1:
			return 'I\'m already responding to direct messages'
		db.setQuiet(chat['id'], 1)
		return 'I\'ll only respond to messages starting with "!"'
	elif text == '!quiet':
		if chat['quiet'] == 2:
			return 'I\'m already quiet'
		db.setQuiet(chat['id'], 2)
		return 'Okay, I\'ll be quiet.'		
	
	
	if chat['quiet'] == 1:
		if text.startswith('!'):
			text = text[1:]
		else:
			return ''
	elif chat['quiet'] == 2:
		return ''
	
	
	waitingFor = userInfo['waitingFor']
	if waitingFor == 'call':
		db.setWaitingFor(userInfo['id'], 'nothing')
		glob.changeNickname(origText, chat, userInfo)
		return genReply('callmesuccess', userInfo, origText)
	elif waitingFor == 'like':
		db.setWaitingFor(userInfo['id'], 'nothing')
		db.addLike(userInfo['id'], origText)
		return genReply('ilike', userInfo, origText)
	elif waitingFor == 'dislike':
		db.setWaitingFor(userInfo['id'], 'nothing')
		db.removeLike(userInfo['id'], origText)
		return genReply('idontlike', userInfo, origText)
	elif waitingFor == 'infix':
		db.setWaitingFor(userInfo['id'], 'nothing')
		ans = util.getInfix(text)
		if ans:
			return 'Answer: {}'.format(ans)
		else:
			return 'Sorry, I couldn\'t parse that infix expression.'
	elif waitingFor == 'postfix':
		db.setWaitingFor(userInfo['id'], 'nothing')
		ans = util.getPostfix(text)
		if ans:
			return 'Answer: {}'.format(ans)
		else:
			return 'Sorry, I couldn\'t parse that postfix expression.'
	elif waitingFor == 'calc':
		db.setWaitingFor(userInfo['id'], 'nothing')
		exp = text.replace('calculate', '').replace('calc', '').replace('what\'s', '').replace('whats', '').strip()
		ans = util.calculate(exp)
		if ans and ans == 42:
			return genReply('42', userInfo)
		elif ans:
			return 'Answer: {}'.format(ans)
		else:
			return 'Sorry, I can\'t solve that!'
		
		
	# Admin Commands
	if userInfo['admin']:
		if text == 'reboot':
			if len(sys.argv) >= 2:
				sys.argv = sys.argv[:1]
			else:
				glob.bm(chat, 'Rebooting...')
				os.execv(sys.executable, ['python3'] + sys.argv[:1] + [str(chat['id'])])
		elif text.startswith('git ') or text.startswith('cat ') or text.startswith('ls'):
			return processOutput(text)
		elif text == 'update' or text == 'refresh' or text == 'reload':
			loadReplies()
			return 'Refreshing Response List Done!'
		elif text.startswith('python'):
			cmd = text[6:]
			try:
				return str(eval(cmd))
			except:
				return 'Error parsing Python code.'
		elif 'volume' in text:
			text = text.replace('volume', '').replace('set', '').replace('to', '').replace('percent', '').replace('%', '').strip()
			try:
				percent = int(text)
				processOutput('amixer sset Master ' + str(percent) + '%')
				return 'Successfully set volume to ' + text + ' percent!'
			except Exception as e:
				print('Volume Error: ', e)
				return 'Couldn\'t set the volume... Sorry!'
		elif text.startswith('text'):
			number = text.split()[1]
			msg = ' '.join(text.split()[2:])
			if len(number) <= 10:
				number = '1' + number
			bots.sms.sendMessage(number, msg)
			return 'Sent Text.'
		
		
	if text.startswith('contest'):
		return contest.getUpcomingContests()
	elif text.startswith('do you like'):
		arg = text[11:].strip().replace('?', '')
		return genReply('doyoulike', userInfo, arg)
	elif text.startswith('say'):
		glob.say(userInfo['firstName'] + ' ' + userInfo['lastName'] + ' says: ' + text[3:])
		return 'Delivered ' + Emoji.happy()
	elif text.startswith('infix'):
		exp = text[5:].strip()
		if not exp:
			db.setWaitingFor(userInfo['id'], 'infix')
			return 'Enter an expression:'
		ans = util.getInfix(exp)
		if ans:
			return 'Answer: {}'.format(ans)
		else:
			return 'Sorry, I couldn\'t parse that infix expression.'
	elif text.startswith('postfix'):
		exp = text[7:]
		if not exp:
			db.setWaitingFor(userInfo['id'], 'postfix')
			return 'Enter an expression:'
		ans = util.getPostfix(exp)
		if ans:
			return 'Answer: {}'.format(ans)
		else:
			return 'Sorry, I couldn\'t parse that postfix expression.'
	elif text.startswith('echo ') or text.startswith('repeat '):
		return text.replace('echo ', '').replace('repeat ', '')
	elif text.startswith('call me') or text.startswith('callme'):
		newName = origText[origText.lower().index('me')+2:].strip()
		if newName != '':
			glob.changeNickname(newName, chat, userInfo)
			return 'Okay, from now on, I\'ll call you ' + newName + '! ' + Emoji.happy()
		else:
			db.setWaitingFor(userInfo['id'], 'call')
			return genReply('callme', userInfo)
	elif text.startswith('time'):
		return util.convertDate(util.getDate())
	elif text.startswith('hi') or text.startswith('hey') or text.startswith('hello'):
		if userInfo['nickName'].lower() == 'bae':
			return genReply('bae', userInfo)
		else:
			return genReply('hello', userInfo)
	elif text.startswith('emoji'):
		emoji = chr(random.randint(0x1F601, 0x1F650))
		if userInfo['type'] == 'm':
			bots.messenger.client.changeThreadEmoji(emoji, thread_id=chat['chatId'])
		return emoji
	elif text.startswith('gravatar'):
		email = text[8:].strip()
		md5 = hashlib.md5()
		md5.update(email.encode('utf-8'))
		glob.sendPhoto(chat, 'https://www.gravatar.com/avatar/' + md5.hexdigest() + '.jpg')
		return ''
	elif text.startswith('meme'):
		glob.sendPhoto(chat, glob.WEBHOOK + 'image/tim.png')
		return ''
	elif text.startswith('rand'):
		data = text.split()
		if len(data) != 3:
			return 'Format should be \"rand [num1] [num2]\".'
		try:
			return str(random.randint(int(data[1]), int(data[2])))
		except:
			return 'Please enter a valid number.'
	elif 'bot' not in text and 'are you a' in text:
		text = text.replace('are you a', '')
		if text[0] == 'n':
			text = text[1:]
		return genReply('areyoua', userInfo, text.strip())
	elif re.match('are.+real', text):
		q = re.match('are(.+)real', text).group(1)
		return genReply('arereal', userInfo, q.strip())
	elif re.match('is.+real', text):
		q = re.match('is(.+)real', text).group(1)
		return genReply('isreal', userInfo, q.strip())
	elif text.startswith('i like') or text.startswith('ilike'):
		like = origText[text.index('like')+4:].strip()
		if like != '':
			db.addLike(userInfo['id'], like)
			return genReply('ilike', userInfo, like)
		else:
			db.setWaitingFor(userInfo['id'], 'like')
			return 'What do you like, ' + userInfo['firstName'] + '?'
	elif text.startswith('i dont like') or text.startswith('idontlike') or text.startswith('i don\'t like'):
		like = origText[text.index('like')+4:].strip()
		if like != '':
			db.removeLike(userInfo['id'], like)
			return genReply('idontlike', userInfo, like)
		else:
			db.setWaitingFor(userInfo['id'], 'dislike')
			return 'What do you not like, ' + userInfo['firstName'] + '?'
	elif text.startswith('likes'):
		likes = db.getLikes(userInfo['id'])
		if len(likes) == 0:
			return 'I don\'t know what you like!'
		else:
			return 'You like ' + str(', '.join(likes))
	elif 'weather' in text:
		try:
			if userInfo['type'] != 'k':
				glob.bm(chat, 'Calculating...')
			if ' in ' in text:
				target = origText[text.rindex(' in ')+4:].strip()
			elif ' at ' in text:
				target = origText[text.rindex(' at ')+4:].strip()
			else:
				target = 'McDonough, GA'
			geolocator = geopy.geocoders.Nominatim()
			location = geolocator.geocode(target)
			weather = glob.owm.weather_around_coords(location.latitude, location.longitude)[0].get_weather()
			temp = weather.get_temperature('fahrenheit')['temp']
			clouds = weather.get_clouds()
			humid = weather.get_humidity()
			status = weather.get_detailed_status().capitalize()
			if temp <= 32: # Cold!
				return genReply('freezing', userInfo, status, str(temp), str(clouds), str(humid), target)
			elif temp <= 60: # Cool and Nice
				return genReply('cool', userInfo, status, str(temp), str(clouds), str(humid), target)
			elif temp <= 85: # Warm and Nice
				return genReply('warm', userInfo, status, str(temp), str(clouds), str(humid), target)
			else: #Hot
				return genReply('hot', userInfo, status, str(temp), str(clouds), str(humid), target)
		except Exception as e:
			print('Weather Error: ', e)
			return 'Couldn\'t get the weather... Try Again?'
	else:
		remindText = reminders.tryParse(chat, text, origText, userInfo, genReply)
		if remindText.strip():
			return remindText
		
		data = ''.join(c for c in text if c.isalnum() or c == ' ').split()
		possible = {}
		for word in data:
			if word in replymap:
				for k in replymap[word].keys():
					possible[k] = possible[k] + 1 if k in possible else 1
		response, percent = '', 0
		for k, v in possible.items():
			p = v / tests[k]
			if p >= percent:
				percent = p
				response = k
		if response:
			return genReply(response, userInfo)
	if text.startswith('calc') or text.startswith('calculate') or text.startswith('what\'s') or text.startswith('whats'):
		exp = text.replace('calculate', '').replace('calc', '').replace('what\'s', '').replace('whats', '').strip()
		if not exp:
			db.setWaitingFor(userInfo['id'], 'calc')
			return 'Enter an expression:'
		ans = util.calculate(exp)
		if ans and ans == 42:
			return genReply('42', userInfo)
		elif ans:
			return 'Answer: {}'.format(ans)
		else:
			return 'Sorry, I can\'t solve that!'
			
	return ''
	

loadReplies()
