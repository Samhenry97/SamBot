import os
import pymysql.cursors
import pymysql

class Database:
	def __init__(self):
		self.open()
		
	#######################################################################################################
	#######################################################################################################
	# SELECT
	
	def selectOne(self, sql, args=None):
		with self.conn.cursor() as cursor:
			cursor.execute(sql, args)
			return cursor.fetchone()
		
	def selectMany(self, sql, args=None):
		with self.conn.cursor() as cursor:
			cursor.execute(sql, args)
			return [row for row in cursor]
			
	def selectAll(self, sql, args=None):
		with self.conn.cursor() as cursor:
			cursor.execute(sql, args)
			return cursor.fetchall()
				
	def getUser(self, id, type):
		return self.selectOne('SELECT * FROM users WHERE userId = %s AND type = %s', (id, type))
		
	def getUserById(self, id):
		return self.selectOne('SELECT * FROM users WHERE id = %s', (id,))

	def getUsersByName(self, name):
		return self.selectMany('SELECT * FROM users WHERE firstName LIKE %s', ('%' + name + '%',))
	
	def getUserByEmail(self, email):
		return self.selectOne('SELECT * FROM users WHERE email = %s', (email,))
		
	def getUserByUserName(self, userName):
		return self.selectOne('SELECT * FROM users WHERE userName = %s', (userName,))
		
	def getUserByEmailOrUserName(self, email):
		return self.selectOne('SELECT * FROM users WHERE email = %s OR userName = %s', (email, email))
		
	def getUserByCreds(self, creds):
		return self.selectOne('SELECT * FROM users WHERE email = %s OR userName = %s', (creds,))
		
	def getAdmins(self):
		return self.selectMany('SELECT * FROM users WHERE admin = TRUE')
		
	def getChat(self, chatId, type):
		return self.selectOne('SELECT * FROM chats WHERE chatId = %s AND type = %s', (chatId, type))
			
	def getChatById(self, chatId):
		return self.selectOne('SELECT * FROM chats WHERE id = %s', (chatId,))

	def getPrivateChatForUser(self, userId):
		return self.selectOne('SELECT * FROM chats INNER JOIN chatusers ON chats.id = chatusers.chatId INNER JOIN users ON users.id = chatusers.userId WHERE users.id = %s', (userId,))
			
	def getUserForPrivateChat(self, chatId):
		return self.selectOne('SELECT * FROM users INNER JOIN chatusers ON users.id = chatusers.userId INNER JOIN chats ON chats.id = chatusers.chatId WHERE chats.id = %s AND chats.public = 0', (chatId,))

	def getAlerts(self):
		return self.selectAll('SELECT * FROM alarms')

	def getLikes(self, userId):
		ans = []
		with self.conn.cursor() as cursor:
			sql = 'SELECT name FROM likes WHERE userId = %s'
			cursor.execute(sql, (userId,))
			for row in cursor:
				ans.append(row['name'])
		return ans

	def loadUsers(self, dict):
		with self.conn.cursor() as cursor:
			sql = 'SELECT userId, type FROM users'
			cursor.execute(sql)
			for row in cursor:
				dict[(row['userId'], row['type'])] = True

	def loadChats(self, dict):
		with self.conn.cursor() as cursor:
			sql = 'SELECT chatId, type FROM chats'
			cursor.execute(sql)
			for row in cursor:
				dict[(row['chatId'], row['type'])] = True
			
	def getAlarms(self, userId=-1, chatId=-1):
		with self.conn.cursor() as cursor:
			if chatId == -1:
				sql = 'SELECT * FROM alarms WHERE userId = %s AND message IS NULL ORDER BY time'
				cursor.execute(sql, (userId,))
				return cursor.fetchall()
			elif userId == -1:
				sql = 'SELECT * FROM alarms WHERE chatId = %s AND message IS NULL ORDER BY time'
				cursor.execute(sql, (chatId,))
				return cursor.fetchall()
			else:
				sql = 'SELECT * FROM alarms WHERE userId = %s AND chatId = %s AND message IS NULL ORDER BY time'
				cursor.execute(sql, (userId, chatId))
				return cursor.fetchall()

	def getReminders(self, userId=-1, chatId=-1):
		with self.conn.cursor() as cursor:
			if chatId == -1:
				sql = 'SELECT * FROM alarms WHERE userId = %s AND message IS NOT NULL ORDER BY time'
				cursor.execute(sql, (userId,))
				return cursor.fetchall()
			elif userId == -1:
				sql = 'SELECT * FROM alarms WHERE chatId = %s AND message IS NOT NULL ORDER BY time'
				cursor.execute(sql, (chatId,))
				return cursor.fetchall()
			else:
				sql = 'SELECT * FROM alarms WHERE userId = %s AND chatId = %s AND message IS NOT NULL ORDER BY time'
				cursor.execute(sql, (userId, chatId))
				return cursor.fetchall()
				
	def getAlertsForUser(self, userId):
		return self.selectMany('SELECT * FROM alarms WHERE userId = %s', (userId,))
				
	def getMessagesForUser(self, userId, offset=0, per=40):
		total = int(self.selectOne('SELECT COUNT(*) AS total FROM messages WHERE userId = %s', (userId,))['total'])
		if total - per - offset < 0:
			per = max(per - abs(total - per - offset), 0)
			offset = 0
		else:
			offset = total - per - offset
		return self.selectMany('SELECT * FROM messages WHERE userId = %s ORDER BY created ASC, fromUser DESC LIMIT {},{}'.format(offset, per), (userId,))
	
	#######################################################################################################
	#######################################################################################################
	# INSERT
	
	def insert(self, sql, args):
		with self.conn.cursor() as cursor:
			cursor.execute(sql, args)
		self.conn.commit()

	def addUser(self, id, first, last, userName, type, email=None, password=None):
		self.insert('INSERT INTO users (userId, firstName, lastName, userName, nickName, type, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (id, first, last, userName, '', type, email, password))
		
	def addLike(self, userId, like):
		self.insert('INSERT INTO likes (name, userId) VALUES (%s, %s)', (like, userId))
		
	def addChat(self, chatId, type, public):
		self.insert('INSERT INTO chats (chatId, type, public) VALUES (%s, %s, %s)', (chatId, type, 1 if public else 0))

	def addChatUser(self, chatId, userId):
		self.insert('INSERT INTO chatusers (chatId, userId) VALUES (%s, %s)', (chatId, userId))
		
	def addReminder(self, userId, chatId, message, time):
		self.insert('INSERT INTO alarms (userId, chatId, message, time) VALUES (%s, %s, %s, %s)', (userId, chatId, message, time))

	def addAlarm(self, userId, chatId, time):
		self.addReminder(userId, chatId, None, time)
		
	def addMessage(self, userId, text, fromUser):
		if text.strip():
			self.insert('INSERT INTO messages (userId, text, fromUser) VALUES (%s, %s, %s)', (userId, text, fromUser))

	#######################################################################################################
	#######################################################################################################
	# UPDATE
	
	def update(self, sql, args):
		with self.conn.cursor() as cursor:
			cursor.execute(sql, args)
		self.conn.commit()

	def setNickname(self, id, nickName):
		self.update('UPDATE users SET nickName = %s WHERE id = %s', (nickName, id))
		
	def setFirstName(self, id, firstName):
		self.update('UPDATE users SET firstName = %s WHERE id = %s', (firstName, id))
		
	def setLastName(self, id, lastName):
		self.update('UPDATE users SET lastName = %s WHERE id = %s', (lastName, id))
		
	def setWaitingFor(self, userId, waitingFor):
		self.update('UPDATE users SET waitingFor = %s WHERE id = %s', (waitingFor, userId))
		
	def setChatUUID(self, chatId, uuid):
		self.update('UPDATE chats SET uuid = %s WHERE id = %s', (uuid, chatId))

	#######################################################################################################
	#######################################################################################################
	# DELETE
	
	def deleteUser(self, userId):
		self.update('DELETE FROM users WHERE id = %s', (userId,))
		
	def deleteUserMessages(self, userId):
		self.update('DELETE FROM messages WHERE userId = %s', (userId,))
	
	def removeLike(self, userId, like):
		with self.conn.cursor() as cursor:
			sql = 'SELECT id FROM likes WHERE name = %s AND userId = %s'
			cursor.execute(sql, (like, userId))
			row = cursor.fetchone()
			if row is not None:
				sql = 'DELETE FROM likes WHERE id = %s'
				cursor.execute(sql, (row['id']))
		self.conn.commit()
		
	def deleteAlarm(self, id):
		with self.conn.cursor() as cursor:
			sql = 'DELETE FROM alarms WHERE id = %s'
			cursor.execute(sql, (id,))
		self.conn.commit()
		
	def clearAlarms(self, userId, chatId=-1):
		with self.conn.cursor() as cursor:
			if chatId == -1:
				sql = 'DELETE FROM alarms WHERE userId = %s AND message IS NULL'
				cursor.execute(sql, (userId,))
			else:
				sql = 'DELETE FROM alarms WHERE userId = %s AND chatId = %s AND message IS NULL'
				cursor.execute(sql, (userId, chatId))
		self.conn.commit()

	def clearReminders(self, userId, chatId=-1):
		with self.conn.cursor() as cursor:
			if chatId == -1:
				sql = 'DELETE FROM alarms WHERE userId = %s AND message IS NOT NULL'
				cursor.execute(sql, (userId,))
			else:
				sql = 'DELETE FROM alarms WHERE userId = %s AND chatId = %s AND message IS NOT NULL'
				cursor.execute(sql, (userId, chatId))
		self.conn.commit()
	
	#######################################################################################################
	#######################################################################################################
	# OTHER
	
	def testConnection(self):
		try:
			self.conn.cursor().execute('SELECT 1')
		except pymysql.err.OperationalError:
			self.close()
			self.open()

	def close(self):
		self.conn.close()

	def open(self):
		self.conn = pymysql.connect(
			host='localhost',
			user='root',
			password='password',
			db='sambot',
			charset='utf8mb4',
			cursorclass=pymysql.cursors.DictCursor)
