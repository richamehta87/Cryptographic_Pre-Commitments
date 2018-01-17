import json
import os
from Message import *
from pprint import pprint

FAILURE = -1
SUCCESS = 1
ALERT = 0

fileName = "dataFile.json"
refIdList = [ i for i in range(100)]


class MessageManager(object):
    def __init__(self):
        pass


    def getFileData(self, fname):
        if os.path.isfile(fname):
            with open(fname) as f:
                data = json.load(f)
            return data
        else:
            return FAILURE


    def addMessage(self, msg):
        if len(refIdList):
            newRefId = refIdList.pop(0)
        else:
            return FAILURE

        newMsg = Message(newRefId, msg)

        newDict = {str(newMsg.refId): [newMsg.encryptedMsg, newMsg.time, newMsg.msgHash]}
        if not os.path.isfile(fileName):
            with open(fileName, 'w') as f:
                json.dump(newDict, f)
        else:
            with open(fileName) as f:
                data = json.load(f)
            data.update(newDict)
            with open(fileName, 'w') as f:
                json.dump(data, f)
        return newRefId


    def getDecodedMessage(self, refId):
        fileData = self.getFileData(fileName)
        if fileData == FAILURE:
            return FAILURE
        if str(refId) in fileData.keys():
            refIdData = fileData[str(refId)]
            encryptedMsg = refIdData[0]
            msg = decodeMsg("encrypt", encryptedMsg)
            return msg
        else:
            return FAILURE


    def deleteMessage(self, refId):
        fileData = self.getFileData(fileName)
        if fileData == FAILURE:
            return FAILURE

        if str(refId) in fileData.keys():
            fileData.__delitem__(str(refId))
            with open(fileName, 'w') as f:
                json.dump(fileData, f)
            refIdList.append(refId)
            return SUCCESS
        else:
            return FAILURE


    def revealMessage(self, refId):
        fileData = self.getFileData(fileName)
        if fileData == FAILURE:
            return FAILURE

        if str(refId) in fileData.keys():
            refIdData = fileData[str(refId)]

            encryptedMsg = refIdData[0]
            msg = decodeMsg("encrypt", encryptedMsg)
            refIdData[0] = msg

            newMsgHash = encodeMsg("hash", msg)
            refIdData[2] = newMsgHash

            newDict = {str(refId):refIdData}

            fileData.__delitem__(str(refId))
            fileData.update(newDict)
            with open(fileName, 'w') as f:
                json.dump(fileData, f)
            return str(msg)
        else:
            return FAILURE


    #API Exposed to 3rd Party
    def getMessageData(self, refId):
        fileData = self.getFileData(fileName)
        if fileData == FAILURE:
            return FAILURE

        if str(refId) in fileData.keys():
            refIdData = fileData[str(refId)]
            result = str(refId) + str(refIdData)
            return result
        else:
            return FAILURE


    #API Exposed to 3rd Party
    def getMessageOnly(self, refId):
        fileData = self.getFileData(fileName)
        if fileData == FAILURE:
            return FAILURE

        if str(refId) in fileData.keys():
            refIdData = fileData[str(refId)]
            result = refIdData[0]
            return result
        else:
            return FAILURE

    # API Exposed to 3rd Party
    def verifyDataIntegrity(self, refId):
        fileData = self.getFileData(fileName)
        if fileData == FAILURE:
            return FAILURE

        if str(refId) in fileData.keys():
            refIdData = fileData[str(refId)]
            encryptedMsg = refIdData[0]
            msgHash = refIdData[2]
            if (encodeMsg("hash", encryptedMsg) == msgHash):
                return SUCCESS
            else:
                return ALERT
        else:
            return FAILURE

    #API Exposed to 3rd Party
    def getTimePosted(self, refId):
        fileData = self.getFileData(fileName)
        if (fileData == FAILURE):
            return FAILURE
        if str(refId) in fileData.keys():
            refIdData = fileData[str(refId)]
            return(refIdData[1])
        else:
            return FAILURE


    #API Exposed to 3rd Party
    def getAllMessages(self):
        fileData = self.getFileData(fileName)
        if (fileData == FAILURE):
            return FAILURE
        return fileData
