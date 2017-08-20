import os, math
import pymysql
import glob, util, reply
from flask import request, Response
from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage, PictureMessage

client = None

def onMessage():
    if not client.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)
        
    messages = messages_from_json(request.json['messages'])

    for kikMessage in messages:
        if not isinstance(kikMessage, TextMessage):
            continue
            
        try:
            db = glob.db
            db.testConnection()
            
            userName = kikMessage.from_user
            userId = util.hash(userName)
            chatUUID = kikMessage.chat_id
            chatId = int(math.sqrt(math.sqrt(math.sqrt(int(chatUUID, 16)))))
            message = kikMessage.body
            
            user = client.get_user(userName)
            info = { 'id': userId, 'first_name': user.first_name, 'last_name': user.last_name, 'username': userName }
            
            userInfo, chat = util.checkDatabase(info, chatId, kikMessage.chat_type != 'direct', 'k')
            if chat['uuid'] is None: # Needed for kik messages
                db.setChatUUID(chat['id'], chatUUID)
            
            print('Kik message from', userInfo['firstName'], userInfo['lastName'])
            print('\tChat ID:', chatId, '(Public)' if kikMessage.chat_type == 'direct' else '(Private)')
            print('\tMessage:', message, '\n')
            
            response = reply.getReply(message, userInfo, chat)
     
            if response:
                sendMessage(userName, chatUUID, response)
        except (ConnectionAbortedError, pymysql.err.OperationalError, pymysql.err.InterfaceError):
            sendMessage(userName, chatUUID, 'Connection lost to the database. Connecting...')
            db.close()
            db.open()
            sendMessage(userName, chatUUID, 'Connected!')
        except Exception as e:
            glob.messageAdmins('Uncaught Error: {}'.format(e))
            sendMessage(userName, chatUUID, 'Sorry, something went wrong... ')

    return Response(status=200)

def sendPhoto(recipient, chatId, url):
    client.send_messages([PictureMessage(to=recipient, chat_id=chatId, pic_url=url)])

def sendMessage(recipient, chatId, message):
    client.send_messages([TextMessage(to=recipient, chat_id=chatId, body=message)])

def init():
    global client
    client = KikApi(os.environ['KIK_USER'], os.environ['KIK_API_KEY'])
    client.set_configuration(Configuration(webhook=glob.WEBHOOK + 'kik'))
