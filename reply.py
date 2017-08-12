import re, random
import glob, reminders
from emoji import Emoji
from expressions import ExpressionSolver, ExpressionTree, InfixToPostfix

replies = {}
tests = {}

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
				tests[key] = line[5:]
			elif line == '{start}':
				inline = True
			else:
				replies[key].append(line)

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

	reply = replaceWithVar(reply, 'fName', info['first_name'])
	reply = replaceWithVar(reply, 'lName', info['last_name'])
	reply = replaceWithVar(reply, 'uName', info['username'])

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
	
	
	
def getReply(chatId, origText, userInfo):
	db = glob.db
	text = origText.lower()
	
	
	waitingFor = db.getWaitingFor(userInfo['id'])['waitingFor']
	if waitingFor == 'call':
		db.setWaitingFor(userInfo['id'], 'nothing')
		db.setNickname(userInfo['id'], origText)
		return genReply('callmesuccess', userInfo, origText)
	elif waitingFor == 'like':
		db.setWaitingFor(userInfo['id'], 'nothing')
		db.addLike(userInfo['id'], origText)
		return genReply('ilike', userInfo, origText)
	elif waitingFor == 'dislike':
		db.setWaitingFor(userInfo['id'], 'nothing')
		db.removeLike(userInfo['id'], origText)
		return genReply('idontlike', userInfo, origText)
	
	
	if text.startswith('do you like'):
		arg = text[11:].strip().replace('?', '')
		return genReply('doyoulike', userInfo, arg)
	elif text.startswith('say'):
		glob.say(userInfo['first_name'] + ' ' + userInfo['last_name'] + ' says: ' + text[3:])
		return 'Delivered ' + Emoji.happy()
	elif text.startswith('calc'):
		try:
			e = ExpressionSolver(text[4:])
			ans = e.solve()
		except:
			return 'Sorry, I can\'t solve that.'
		else:
			if ans == 42:
				return genReply('42', userInfo)
			else:
				return 'Answer: ' + str(ans)
	elif text.startswith('infix'):
		i = InfixToPostfix(text[5:].strip())
		try:
			return 'Postfix: ' + i.genPostfix()
		except:
			return 'Error parsing infix expression.'
	elif text.startswith('postfix'):
		try:
			e = ExpressionTree(text[7:].strip())
			return 'Answer: ' + str(e.eval())
		except:
			return 'Error parsing postfix expression.'
	elif 'valid' in text:
		return genReply('valid', userInfo)
	elif text.startswith('ls'):
		ans = ['Files in current directory: ', '']
		for file in os.listdir('.'):
			ans.append(file)
		return '\n'.join(ans)
	elif text.startswith('cat '):
		fileName = origText[4:]
		try:
			with open(fileName) as file:
				contents = file.read().replace(TOKEN, '{{HIDDEN INFORMATION}}')
				return contents
		except FileNotFoundError:
			return 'Could not find "{}"'.format(fileName)
	elif text.startswith('echo ') or text.startswith('repeat '):
		return text.replace('echo ', '').replace('repeat ', '')
	elif text.startswith('call me') or text.startswith('callme'):
		newName = origText[origText.lower().index('me')+2:].strip()
		if newName != '':
			db.setNickname(userInfo['id'], newName)
			return 'Okay, from now on, I\'ll call you ' + newName + '! ' + Emoji.happy()
		else:
			db.setWaitingFor(userInfo['id'], 'call')
			return genReply('callme', userInfo)
	elif text.startswith('time'):
		return str(util.getDate())
	elif text.startswith('tim'):
		return genReply('tim', userInfo)
	elif '\U0001f611' in text:
		return genReply('annoying', userInfo)
	elif text.startswith('hi') or text.startswith('hey') or text.startswith('hello'):
		user = db.getUser(userInfo['id'])
		if user['nickName'].lower() == 'bae':
			return genReply('bae', userInfo)
		else:
			return genReply('hello', userInfo, user['nickName'])
	elif text.startswith('emoji'):
		return chr(random.randint(0x1F601, 0x1F650))
	elif text.startswith('gravatar'):
		#email = text[8:].strip()
		#md5 = hashlib.md5()
		#md5.update(email.encode('utf-8'))
		#await glob.bot.sendPhoto(chatId, 'https://www.gravatar.com/avatar/' + md5.hexdigest() + '.jpg')
		return 'Feature Disabled'
	elif text.startswith('rand'):
		data = text.split()
		if len(data) != 3:
			return 'Format should be \"rand [num1] [num2]\".'
		try:
			return str(random.randint(int(data[1]), int(data[2])))
		except:
			return 'Please enter a valid number.'
	elif 'emotion' in text:
		return genReply('emotion', userInfo)
	elif text.startswith('i like') or text.startswith('ilike'):
		like = origText[text.index('like')+4:].strip()
		if like != '':
			db.addLike(userInfo['id'], like)
			return genReply('ilike', userInfo)
		else:
			db.setWaitingFor(userInfo['id'], 'like')
			return 'What do you like, ' + userInfo['first_name'] + '?'
	elif text.startswith('i dont like') or text.startswith('idontlike') or text.startswith('i don\'t like'):
		like = origText[text.index('like')+4:].strip()
		if like != '':
			db.removeLike(userInfo['id'], like)
			return genReply('idontlike', userInfo, like)
		else:
			db.setWaitingFor(userInfo['id'], 'dislike')
			return 'What do you not like, ' + userInfo['first_name'] + '?'
	elif text.startswith('likes'):
		likes = db.getLikes(userInfo['id'])
		if len(likes) == 0:
			return 'I don\'t know what you like!'
		else:
			return 'You like ' + str(', '.join(likes))
	elif text.startswith('locate'):
		#r = requests.get('http://freegeoip.net/json')
		#j = json.loads(r.text)
		#await glob.bot.sendLocation(chatId, j['latitude'], j['longitude'])
		return 'Feature Disabled'
	elif '\U0001f602' in text:
		return '\U0001f602' * random.randint(1, 5)
	elif text.startswith('weather'):
		try:
			r = requests.get('http://freegeoip.net/json')
			j = json.loads(r.text)
			weather = glob.owm.weather_around_coords(j['latitude'], j['longitude'])[0].get_weather()
			temp = weather.get_temperature('fahrenheit')['temp']
			clouds = weather.get_clouds()
			humid = weather.get_humidity()
			status = weather.get_detailed_status()
			if temp <= 32: # Cold!
				return genReply('freezing', userInfo, status, str(temp), str(clouds), str(humid))
			elif temp <= 60: # Cool and Nice
				return genReply('cool', userInfo, status, str(temp), str(clouds), str(humid))
			elif temp <= 85: # Warm and Nice
				return genReply('warm', userInfo, status, str(temp), str(clouds), str(humid))
			else: #Hot
				return genReply('hot', userInfo, status, str(temp), str(clouds), str(humid))
		except:
			return 'Couldn\'t get the weather... Try Again?'
	else:
		remindText = reminders.tryParse(chatId, text, origText, userInfo, genReply)
		if remindText.strip():
			return remindText
		
		for k, v in tests.items():
			if v != 'manual' and eval(v):
				return genReply(k, userInfo)
	return ''
	

loadReplies()
