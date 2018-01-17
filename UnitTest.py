from MessageManager import *
from pprint import pprint


def testMessageManager():
    msgManager = MessageManager()
    id1 = msgManager.addMessage("Hello World")
    assert id1 == 0

    id2 = msgManager.addMessage("World")
    assert id2 == 1

    id3 = msgManager.addMessage("Richa")
    assert id3 == 2

    id4 = msgManager.addMessage("Here")
    assert id4 == 3

    msg1 = msgManager.getMessageOnly(id1)
    assert msg1 == "­ÓÏÞèËÔàÏÖ"

    msg2 = msgManager.revealMessage(id2)
    assert msg2 == "World"

    msg3 = msgManager.getDecodedMessage(id3)
    assert msg3 == "Richa"

    del1 = msgManager.deleteMessage(id4)
    assert del1 == SUCCESS

    integrity3 = msgManager.verifyDataIntegrity(id2)
    assert integrity3 == SUCCESS

    allMsgs = msgManager.getAllMessages()
    print ("\nCongratulations !!!\nIf you reached here, all operations defined in this Test Framework were successful\n\n")
    print ("Current Message Data     in the Database:\n\n")
    pprint (allMsgs)
    print("\nSince you revealed message for Ref ID: 1, you are seeing the plain text message for it.")



if __name__ == "__main__":
    testMessageManager()
