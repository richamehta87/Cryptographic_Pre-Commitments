from datetime import datetime

def encodeMsg(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    return encoded_string



def decodeMsg(key, enc):
    dec = []
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)



class Message(object):

    def __init__(self, refId, message):
        self.refId = refId
        self.encryptedMsg = encodeMsg("encrypt", message)
        now = datetime.now()
        self.time = now.strftime("%c")
        self.msgHash = encodeMsg("hash", self.encryptedMsg)

    def setRefId(self, refId):
        self.redId = refId

    def getRefId(self):
        return self.refId

    def getMessage(self):
        return self.encryptedMsg

    def setMessage(self, message):
        self.encryptedMsg = encodeMsg("encrypt", message)
