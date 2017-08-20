import os
import pymysql
import glob, util, reply
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
from yowsup.stacks import YowStackBuilder
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.env import YowsupEnv

stack = None
client = None

class WhatsAppSamBot(YowInterfaceLayer):
    @ProtocolEntityCallback("message")
    def onMessage(self, waMessage):
        receipt = OutgoingReceiptProtocolEntity(waMessage.getId(), waMessage.getFrom(), 'read', waMessage.getParticipant())
        
        if waMessage.getType() != 'text':
            return
            
        try:
            db = glob.db
            db.testConnection()
            
            userName = waMessage.getAuthor()
            userId = int(userName.replace('@s.whatsapp.net', ''))
            chatUUID = waMessage.getFrom()
            chatId = chatUUID.replace('@s.whatsapp.net', '').replace('@g.us', '').replace('-', '')
            if len(chatId) > 17:
                chatId = chatId[len(chatId)-17:]
            chatId = int(chatId)
            firstName = waMessage.getNotify().split()[0]
            lastName = ' '.join(waMessage.getNotify().split()[1:])
            message = waMessage.getBody()
            
            info = { 'id': userId, 'first_name': firstName, 'last_name': lastName, 'username': userName }
            userInfo, chat = util.checkDatabase(info, chatId, waMessage.isGroupMessage(), 'w')
            
            if chat['uuid'] is None: # Needed for whatsapp messages
                db.setChatUUID(chat['id'], chatUUID)
                
            print('WhatsApp message from', userInfo['firstName'], userInfo['lastName'])
            print('\tChat ID:', chatId, '(Public)' if waMessage.isGroupMessage() else '(Private)')
            print('\tMessage:', message, '\n')
            
            response = reply.getReply(message, userInfo, chat)
            
            if response:
                sendMessage(chatUUID, response)
        except (ConnectionAbortedError, pymysql.err.OperationalError, pymysql.err.InterfaceError):
            sendMessage(chatUUID, 'Connection lost to the database. Connecting...')
            db.close()
            db.open()
            sendMessage(chatUUID, 'Connected!')
        except Exception as e:
            glob.messageAdmins('Uncaught Error: {}'.format(e))
            sendMessage(chatUUID, 'Sorry, something went wrong... ')
        
        self.toLower(receipt)
        
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)
    
        
def sendMessage(chatId, message):
    client.toLower(TextMessageProtocolEntity(message, to=chatId))

def init():
    global client, stack
    credentials = (os.environ['YOWSUP_NUMBER'], os.environ['YOWSUP_PASS'])
    stackBuilder = YowStackBuilder()
    stack = stackBuilder.pushDefaultLayers(True).push(WhatsAppSamBot).build()
    stack.setCredentials(credentials)
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
    client = stack.getLayer(8)
    
def listen():
    stack.loop()
