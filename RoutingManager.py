from flask import Flask, url_for, request
from MessageManager import *
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome to Precommitment World\n\n'


@app.route('/postMessage' , methods = ['POST'])
def api_postMessageData():
    if request.headers['Content-Type'] == 'text/plain':
        msgManager = MessageManager()
        result = msgManager.addMessage(str(request.data))
        if result == FAILURE:
            return ("Failure posting the message\n\n")
        else:
            return ("Message posted successfully, Save the Ref ID: %s\n\n" % str(result))
    else:
        return("Content type Plain Text allowed\n\n")


@app.route('/getMessageOnly/<refId>')
def api_getMessageOnly(refId):
    msgManager = MessageManager()
    msg = msgManager.getMessageOnly(int(refId))
    if (msg == FAILURE):
        return ("Failure retrieving Message for Ref ID: %s\n\n" % refId)
    else:
        return str(msg + "\n\n")


@app.route('/getMessageData/<refId>')
def api_getMessageData(refId):
    msgManager = MessageManager()
    msgData = msgManager.getMessageData(int(refId))
    if (msgData == FAILURE):
        return ("Failure retrieving Message Data for Ref ID: %s\n\n" % refId)
    else:
        return str(msgData + "\n\n")



@app.route('/getTimePosted/<refId>')
def api_getTimePosted(refId):
    msgManager = MessageManager()
    time = msgManager.getTimePosted(int(refId))
    if time == FAILURE:
        return ("Failure retrieving Time Posted for RefId: %s\n\n" % refId)
    else:
        return str(time + "\n\n")


@app.route('/verifyDataIntegrity/<refId>')
def api_verifyDataIntegrity(refId):
    msgManager = MessageManager()
    result = msgManager.verifyDataIntegrity(int(refId))
    if (result == FAILURE):
        return ("Failure while verifying data integrity for refId: %s\n\n" % refId)
    elif (result == ALERT):
        return ("Data has been tampered for RefId: %s\n\n" % refId)
    else:
        return ("Data integrity verification successful for RefId: %s\n\n" % refId)


@app.route('/deleteMessage/<refId>')
def api_deleteMessage(refId):
    msgManager = MessageManager()
    result = msgManager.deleteMessage(int(refId))
    if (result == FAILURE):
        return ("Failure deleting the message for RefId: %s\n\n" % refId)
    else:
        return ("Message deleted successfully for RefId: %s\n\n" % refId)


@app.route('/revealMessage/<refId>')
def api_revealMessage(refId):
    msgManager = MessageManager()
    result = msgManager.revealMessage(int(refId))
    if (result == FAILURE):
        return ("Failure revealing the message for RefId: %s\n\n" % refId)
    else:
        return ("Message revealed successfully in the database for RefId: %s, \nMessage is: %s\n\n" % (refId, result))


@app.route('/getDecodedMessage/<refId>')
def api_getDecodedMessage(refId):
    msgManager = MessageManager()
    result = msgManager.getDecodedMessage(int(refId))
    if (result == FAILURE):
        return ("Failure revealing the message for RefId: %s\n\n" % refId)
    else:
        return ("For RefId: %s, \nDecoded Message is: %s\n\n" % (refId, result))


if __name__ == '__main__':
    app.run()
