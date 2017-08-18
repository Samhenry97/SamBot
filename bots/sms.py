import os
import pymysql, reply
import glob, util
from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client

client = None
number = os.environ['TWILIO_NUMBER']

def onMessage():
    try:
        db = glob.db
        
        number = request.form['From']
        message = request.form['Body']
        city = request.form['FromCity']
        
        userId = int(number.replace('+', ''))
        chatId = userId
        info = { 'id': userId, 'first_name': '', 'last_name': '', 'username': city }
     
        userInfo, chat = util.checkDatabase(info, chatId, False, 's')
     
        print('Twilio text from', number)
        print('\tChat ID:', number, '(Private)')
        print('\tMessage:', message, '\n')
        
        if not userInfo['firstName'] and not userInfo['lastName'] and userInfo['waitingFor'] == 'nothing': # New User
            db.setWaitingFor(userInfo['id'], 'firstName')
            return generateMessage('Hello! I\'m SamBot! What\'s your first name?')
        elif userInfo['waitingFor'] == 'firstName':
            db.setFirstName(userInfo['id'], message)
            db.setWaitingFor(userInfo['id'], 'lastName')
            return generateMessage('Sweet! And what\'s your last name?')
        elif userInfo['waitingFor'] == 'lastName':
            db.setLastName(userInfo['id'], message)
            db.setWaitingFor(userInfo['id'], 'nothing')
            return generateMessage('Sounds good! I\'ll remember that.')
     
        response = reply.getReply(chatId, message, userInfo, chat)
     
        if response:
            return generateMessage(response)
    except (ConnectionAbortedError, pymysql.err.OperationalError, pymysql.err.InterfaceError):
        message(number, 'Connection lost to the database. Connecting...')
        db.close()
        db.open()
        message(number, 'Connected!')
    except Exception as e:
        glob.messageAdmins('Uncaught Error: {}'.format(e))
        message(number, 'Sorry, something went wrong...')
    return ''

def generateMessage(text):
    response = MessagingResponse()
    response.message(text)
    return str(response)

def sendMessage(recipient, message):
    client.messages.create(to='+' + str(recipient), from_=number, body=message)

def init():
	global client
	client = Client(os.environ['TWILIO_SID'], os.environ['TWILIO_AUTH_TOKEN'])
