import re, random, requests, json, sys, os, subprocess, hashlib, time
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
	
	
	
def getReply(chatId, origText, userInfo):
	db = glob.db
	chat = db.getChat(chatId, userInfo['type'])
	text = origText.lower().strip()
	
	
	waitingFor = userInfo['waitingFor']
	if waitingFor == 'call':
		db.setWaitingFor(userInfo['id'], 'nothing')
		glob.changeNickname(origText, chat['chatId'], userInfo)
		return genReply('callmesuccess', userInfo, origText)
	elif waitingFor == 'like':
		db.setWaitingFor(userInfo['id'], 'nothing')
		db.addLike(userInfo['id'], origText)
		return genReply('ilike', userInfo, origText)
	elif waitingFor == 'dislike':
		db.setWaitingFor(userInfo['id'], 'nothing')
		db.removeLike(userInfo['id'], origText)
		return genReply('idontlike', userInfo, origText)
		
		
	# Admin Commands
	if userInfo['id'] in glob.ADMIN_IDS:
		if text == 'reboot':
			if len(sys.argv) >= 2:
				sys.argv = sys.argv[:1]
			else:
				glob.bm(chat['id'], 'Rebooting...')
				os.execv(sys.executable, ['python3'] + sys.argv[:1] + [str(chat['id'])])
		elif text.startswith('git '):
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
				processOutput('amixer -D pulse sset Master ' + str(percent) + '%')
				return 'Successfully set volume to ' + text + ' percent!'
			except Exception as e:
				print('Volume Error: ', e)
				return 'Couldn\'t set the volume... Sorry!'
		
		
	if text.startswith('do you like'):
		arg = text[11:].strip().replace('?', '')
		return genReply('doyoulike', userInfo, arg)
	elif text.startswith('say'):
		glob.say(userInfo['firstName'] + ' ' + userInfo['lastName'] + ' says: ' + text[3:])
		return 'Delivered ' + Emoji.happy()
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
			glob.changeNickname(newName, chat['id'], userInfo)
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
		if userInfo['nickName'].lower() == 'bae':
			return genReply('bae', userInfo)
		else:
			return genReply('hello', userInfo)
	elif text.startswith('emoji'):
		return chr(random.randint(0x1F601, 0x1F650))
	elif text.startswith('gravatar'):
		email = text[8:].strip()
		md5 = hashlib.md5()
		md5.update(email.encode('utf-8'))
		glob.sendPhoto(chat, 'https://www.gravatar.com/avatar/' + md5.hexdigest() + '.jpg', True)
		return ''
	elif text.startswith('meme'):
		glob.sendPhoto(chat, 'res/tim.png', False)
		return ''
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
	elif '\U0001f602' in text:
		return '\U0001f602' * random.randint(1, 5)
	elif 'weather' in text:
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
		except Exception as e:
			print(e)
			return 'Couldn\'t get the weather... Try Again?'
	else:
		remindText = reminders.tryParse(chat, text, origText, userInfo, genReply)
		if remindText.strip():
			return remindText
		
		for k, v in tests.items():
			if v != 'manual' and eval(v):
				return genReply(k, userInfo)
	if text.startswith('calc') or text.startswith('calculate') or text.startswith('what\'s') or text.startswith('whats'):
		exp = text.replace('calculate', '').replace('calc', '').replace('what\'s', '').replace('whats', '').strip()
		exp = exp.replace('times', '*').replace('minus', '-').replace('to the', '^').replace('power', '').replace('divided by', '/').replace('plus', '+').replace('th', '')
		try:
			e = ExpressionSolver(exp)
			ans = e.solve()
		except:
			return 'Sorry, I can\'t solve that!'
		else:
			if ans == 42:
				return genReply('42', userInfo)
			else:
				return 'Answer: ' + str(ans)
	return ''
	

loadReplies()
