from database import Database
import telepot

TOKEN = '265155953:AAFp_YxsPmVO8N4k6y6fkPIyXKBcumnif8Y'

db = Database()
users = {}
chats = {}
chatUsers = {}
db.loadUsers(users)
db.loadChats(chats)
db.loadChatUsers(chatUsers)

bot = telepot.Bot(TOKEN)

print('Enter any command:')
s = input()
while s.lower() != 'quit':
	if s.startswith('message'):
		u = db.getUsersByName(s.split()[1])
		msg = bytes(' '.join(s.split()[2:]), "utf-8").decode("unicode_escape")
		if len(u) == 1:
			chat = db.getPrivateChat(u[0]['id'])
			bot.sendMessage(chat['id'], msg)
		elif len(u) == 0:
			print('Could not find user.')
		else:
			print('Which User? (select number)')
			for i in range(len(u)):
				print('(%d) %s %s' % (i, u[i]['firstName'], u[i]['lastName']))
			ans = int(input())
			if ans >= 0 and ans < len(u):
				chat = db.getPrivateChat(u[ans]['id'])
				bot.sendMessage(chat['id'], msg)
			else:
				print('Please enter a correct user.')
	s = input()