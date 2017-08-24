import sys
import glob
from datetime import datetime, timedelta
from expressions import ExpressionSolver, ExpressionTree, InfixToPostfix

class Loader:
	def __init__(self, message):
		self.message = message
	
	def __enter__(self):
		print('Loading {}...'.format(self.message))
	
	def __exit__(self, type, value, traceback):
		print('Done!\n')

words = {}

units = [
	"zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
	"nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
	"sixteen", "seventeen", "eighteen", "nineteen",
]
tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
scales = ["hundred", "thousand", "million", "billion", "trillion"]

words["and"] = (1, 0)
words["a"] = (1, 2)
words["few"] = (1, 2)
for i, word in enumerate(units): words[word] = (1, i)
for i, word in enumerate(tens): words[word] = (1, i * 10)
for i, word in enumerate(scales): words[word] = (10 ** (i * 3 or 2), 0)

def textToInt(text):
	text = text.replace('-', ' ')

	current = result = 0
	for word in text.split():
		if word not in words:
			return None
		scale, increment = words[word]
		current = current * scale + increment
		if scale > 100:
			result += current
			current = 0

	return result + current

times = {'noon': 12, 'afternoon': 15, 'midnight': 0, 'sunrise': 6, 'sunset': 18, 'dawn': 6, 'dusk': 18}
dayOffsets = {'today': 0, 'tomorrow': 1, 'next week': 7, 'next month': 31, 'next year': 365}

def getDate(date=None):
	if date == None:
		date = datetime.now()
	return date.replace(microsecond=0)
	
def convertDate(date):
	return date.strftime('%A, %b %d, %Y at %H:%M:%S %p')

def dateFromNow(amount, units):
	try:
		amount = int(amount)
	except:
		amount = textToInt(amount)
	if units[-1] != 's':
		units += 's'
	return getDate() + timedelta(**{ units: amount })

def dateWithOffset(h, m, s, ampm, timeOfDay, offset):
	h = int(h) if h else 0
	m = int(m) if m else 0
	s = int(s) if s else 0
	if timeOfDay:
		date = getDate().replace(hour=times[timeOfDay], minute=0, second=0)
	else:
		date = getDate().replace(hour=h, minute=m, second=s)
		if ampm and ampm == 'pm':
			date += timedelta(hours=12)
	if offset:
		date += timedelta(days=dayOffsets[offset])
	return date
	
def checkDatabase(info, chatId, public, type):
	db = glob.db
	addChatUser = False
	if (chatId, type) not in glob.chats:
		print('Adding Chat: ' + str(chatId))
		addChatUser = True
		db.addChat(chatId, type, public)
		glob.chats[(chatId, type)] = True
	if (info['id'], type) not in glob.users:
		print('Adding User: ' + str(info['id']))
		addChatUser = True
		db.addUser(info['id'], info['first_name'], info['last_name'], info['username'], type)
		glob.users[(info['id'], type)] = True
		glob.messageAdmins('New {} User: {} {}: {} ({})'.format(glob.PLATFORMS[type], info['first_name'], info['last_name'], info['username'], chatId))
	if addChatUser:
		print('Adding Chat User:', chatId, ',', info['id'])
		db.addChatUser(db.getChat(chatId, type)['id'], db.getUser(info['id'], type)['id'])
	return (db.getUser(info['id'], type), db.getChat(chatId, type))
	
def hash(s):
	ans = 1125899906842597
	for c in s:
		ans = ans * 31 + ord(c)
	return (ans & 0xFFFFFFFFFFFFFFF) ^ ((ans & (0xFFFFFFFFFFFFFFF << 32)) >> 32)
	
def getInfix(exp):
	i = InfixToPostfix(exp)
	try:
		return i.genPostfix()
	except:
		return None
		
def getPostfix(exp):
	try:
		e = ExpressionTree(exp)
		return e.eval()
	except:
		return None
	
def calculate(exp):
	exp = exp.replace('times', '*').replace('minus', '-').replace('to the', '^').replace('power', '').replace('divided by', '/').replace('plus', '+').replace('th', '')
	try:
		e = ExpressionSolver(exp)
		return e.solve()
	except:
		return None
