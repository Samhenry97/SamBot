import pymysql.cursors
import pymysql
import os

class Database:
	def __init__(self):
		self.open()
		
	#######################################################################################################
	#######################################################################################################
	# SELECT
	
	def getUser(self, id, type):
		with self.conn.cursor() as cursor:
			sql = 'SELECT * FROM users WHERE userId = %s AND type = %s'
			cursor.execute(sql, (id, type))
		return cursor.fetchone()
		
	def getUserById(self, id):
		with self.conn.cursor() as cursor:
			sql = 'SELECT * FROM users WHERE id = %s'
			cursor.execute(sql, (id))
		return cursor.fetchone()

	def getUsersByName(self, name):
		ans = []
		with self.conn.cursor() as cursor:
			sql = 'SELECT * FROM users WHERE firstName LIKE %s'
			cursor.execute(sql, ('%' + name + '%',))
			for row in cursor:
				ans.append(row)
		return ans
		
	def getChat(self, chatId, type):
		with self.conn.cursor() as cursor:
			sql = 'SELECT * FROM chats WHERE chatId = %s AND type = %s'
			cursor.execute(sql, (chatId, type))
			return cursor.fetchone()
			
	def getChatById(self, chatId):
		with self.conn.cursor() as cursor:
			sql = 'SELECT * FROM chats WHERE id = %s'
			cursor.execute(sql, (chatId))
		return cursor.fetchone()

	def getPrivateChatForUser(self, userId):
		with self.conn.cursor() as cursor:
			sql = 'SELECT * FROM chats INNER JOIN chatusers ON chats.id = chatusers.chatId INNER JOIN users ON users.id = chatusers.userId WHERE users.id = %s'
			cursor.execute(sql, (userId,))
			return cursor.fetchone()

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
				
	def getLikes(self, userId):
		ans = []
		with self.conn.cursor() as cursor:
			sql = 'SELECT name FROM likes WHERE userId = %s'
			cursor.execute(sql, (userId,))
			for row in cursor:
				ans.append(row['name'])
		return ans
			
	def getAlerts(self):
		with self.conn.cursor() as cursor:
			sql = 'SELECT * FROM alarms'
			cursor.execute(sql)
			return cursor.fetchall()
			
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
	
	#######################################################################################################
	#######################################################################################################
	# INSERT

	def addUser(self, id, first, last, userName, type):
		with self.conn.cursor() as cursor:
			sql = 'INSERT INTO users (userId, firstName, lastName, userName, nickName, type) VALUES (%s, %s, %s, %s, %s, %s)'
			cursor.execute(sql, (id, first, last, userName, '', type))
		self.conn.commit()
		
	def addLike(self, userId, like):
		with self.conn.cursor() as cursor:
			sql = 'INSERT INTO likes (name, userId) VALUES (%s, %s)'
			cursor.execute(sql, (like, userId))
		self.conn.commit()
		
	def addChat(self, chatId, type, public):
		with self.conn.cursor() as cursor:
			sql = 'INSERT INTO chats (chatId, type, public) VALUES (%s, %s, %s)'
			cursor.execute(sql, (chatId, type, 1 if public else 0))
		self.conn.commit()

	def addChatUser(self, chatId, userId):
		with self.conn.cursor() as cursor:
			sql = 'INSERT INTO chatusers (chatId, userId) VALUES (%s, %s)'
			cursor.execute(sql, (chatId, userId))
		self.conn.commit()
		
	def addReminder(self, userId, chatId, message, time):
		with self.conn.cursor() as cursor:
			sql = 'INSERT INTO alarms (userId, chatId, message, time) VALUES (%s, %s, %s, %s)'
			cursor.execute(sql, (userId, chatId, message, time))
		self.conn.commit()

	def addAlarm(self, userId, chatId, time):
		self.addReminder(userId, chatId, None, time)

	#######################################################################################################
	#######################################################################################################
	# UPDATE

	def setNickname(self, id, nickName):
		with self.conn.cursor() as cursor:
			sql = 'UPDATE users SET nickName = %s WHERE id = %s'
			cursor.execute(sql, (nickName, id))
		self.conn.commit()
		
	def setFirstName(self, id, firstName):
		with self.conn.cursor() as cursor:
			sql = 'UPDATE users SET firstName = %s WHERE id = %s'
			cursor.execute(sql, (firstName, id))
		self.conn.commit()
		
	def setLastName(self, id, lastName):
		with self.conn.cursor() as cursor:
			sql = 'UPDATE users SET lastName = %s WHERE id = %s'
			cursor.execute(sql, (lastName, id))
		self.conn.commit()
		
	def setWaitingFor(self, userId, waitingFor):
		with self.conn.cursor() as cursor:
			sql = 'UPDATE users SET waitingFor = %s WHERE id = %s'
			cursor.execute(sql, (waitingFor, userId))
		self.conn.commit()

	#######################################################################################################
	#######################################################################################################
	# DELETE
	
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
			charset='utf8',
			cursorclass=pymysql.cursors.DictCursor)
