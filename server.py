import flask
import bots.sms, bots.kik

server = flask.Flask(__name__) # For SMS and Kik
@server.route('/sms', methods=['GET', 'POST'])
def smsMessage():
	return bots.sms.onMessage()
	
@server.route('/kik', methods=['GET', 'POST'])
def kikMessage():
	return bots.kik.onMessage()

def listen():
    server.run()
