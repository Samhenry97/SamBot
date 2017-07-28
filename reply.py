import re
import random
from emoji import Emoji

replies = {}
tests = {}
filler = {}

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
			elif line == 'filler':
				filler[key] = True
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

emojiRegex = re.compile('\{Emoji\.(.+)\}(\(([0-9]+)(,([0-9]+))?\))?')
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
		return Emoji.get(m.group(1)) * random.randint(x, y)
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

loadReplies()