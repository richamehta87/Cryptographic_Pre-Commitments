# Cryptographic_Pre-Commitments
RESTful APIs that demo principles of cryptographic pre-commitments

PROJECT DEFINITION

This project is a prototype for a service that allows the posting of cryptographic pre-commitments (https://en.wikipedia.org/wiki/Commitment_scheme).
There are 2 users of this system --
1. Committer -- Can commit the message to the database, which gets stored in encrypted form
		Can read decrypted message anytime he wants, using the Ref ID of the message
		Can reveal the message in the database, when asked by 3rd Party to reveal it
2. 3rd Party -- Can check the time when Message was posted by the Committer (need Ref ID from Committer for this Message)
		Can verify the Data Inegrity of the Message
		Can read Message in the encrypted form until revealed by the Committer



PROJECT REQUIREMENTS

As a committer I want to post secret messages.
--> Fulfilled

As a committer I want to uniquely reference my messages, such that I can ask 3rd parties to verify my posts.
--> Fulfilled

As a committer I want to ensure that the plaintext of my messages are not readable until I make them so.
--> Fulfilled

As a committer I want a way to irrevocably make an individual secret message publicly readable.
--> Fulfilled

As a 3rd party I want to verify when a message was posted and that it hasn't been tampered with since.
--> Fulfilled

As a 3rd party or committer I want this API to be consumable using no required software beyond cURL.
--> Fulfilled

For the sake of this exercise, assume that all incoming connections were terminated with a TLS connection.
--> Fulfilled



MY PROJECT LIMITATIONS:

1. The user based restrictions have not been coded such that as of now, even 3rd party can consume all the APIs.
2. No Login or Logout for a user, such that any user can see any other user's message data. Login session not maintained
3. Failure scenarios have been extensively tested but not recorded in the UnitTest.py
	

GETTING STARTED

Prerequisites:
1. Python 3.5 installed in the system

Running the Program:
1. Command: "python3.5 RoutingManager.py" --> This will run the localhost web server on port 5000

Running the Tests:
1. Command: "python3.5 UnitTest.py" --> This will run all the unit tests defined in UnitTest.py python file

Breakdown of Code:
1. Message.py -- 'Message' class defines individual Message entity
		 Contains function to encrypt the Message before adding to the database,
		 Contains function to decrypt the Message after reading from the database

2. MessageManager.py -- 'MessageManager' class defines all the functions needed to manage a message.
			Message Management functions like:
			
			For Committer:
			Adding a Message to the Database, (addMessage)
			Deleting a Message from the Database, (deleteMessage)
			Reading an encrypted version of Message, given the RefID of the Message, (getMessage or getMessageData)
			Reading decoded version of Message, given the RedId of the Message, (getDecodedMessage)
			Irrevocably Revealing the Message in the Database to be consumed by 3rd Party any time, (revealMessage)
			
			For 3rd Party User:
			Reading an encrypted version of Message, given the RefID of the Message, (getMessage or getMessageData)
			Verify Data Integrity of the Message given it's Ref ID, (verifyDataIntegrity)
			Get the Time Posted for a Message given the Ref ID, (getTimePosted)
			Get the data of all Messages from teh Database (getAllMessages)

			Managing Reference ID for Message:
			A new Reference ID gets created every time a new Message gets created and added.
			Reference ID is read from a ppol of reference IDs (Python List)
			Once any Message gets deleted that Ref ID gets appended tot he pool of Reference IDs
			Total number of Reference IDs available in a pool = 100
			Hence at a given point of time database cannot have more than 100 messages.
			(ps: This is just a limitation defined currently, it can be extended later)

3. RoutingManager.py -- This python file runs the server and defines the web frameowork REST APIs that calls 'MessageManager' APIs underneath

4. dataFile.json -- Database File to store, edit and retrieve each Message data. Database File instance will remain permanent.

5. UnitTest.py -- Contains a simple UnitTest function that tests all the 'MessageManager' APIs.


6. CURL calls -- Example of CURl calls you can make to the server:
		 All the CURL calls can be accessible by the Committer

		 1. Post a Message and get REF ID.
		    (Message is 'Hello World')
		    Command --> curl -H "Content-type:text/plain" -X POST http://127.0.0.1:5000/postMessage -d 'Hello World' 
		    Output --> Message posted successfully, Save the Ref ID: 0
		
		 2. Get Message which is stored in Encrypted Format.
		    (ps: Use Ref ID 0, that we received in previous curl call)
		    Command --> curl http://127.0.0.1:5000/getMessageOnly/0
		    Output --> Ç«×åÜãÅÒäå

		 3. Get Complete Message Data stored in Database
		    Command --> curl http://127.0.0.1:5000/getMessageData/0
		    Output --> 0['Ç\x95«×åÜã\x85ÅÒäåÔ\x9b', 'Mon Apr 17 08:55:24 2017', 'įöĞĿōĽŖíĭĳŗōļü']

		 4. Get Decoded Message, but don't reveal yet
		    Command --> curl http://127.0.0.1:5000/getDecodedMessage/0
		    Output --> For RefId: 0, 
			       Decoded Message is: b'Hello World'
		
		 5. Reveal the Message in the Database permanently
		    Command --> curl http://127.0.0.1:5000/revealMessage/0
		    Output --> Message revealed successfully in the database for RefId: 0, 
			       Message is: b'Hello World'
		
		 6. Delete the Message from Database
		    Command --> curl http://127.0.0.1:5000/deleteMessage/0
		    Output --> Message deleted successfully for RefId: 0



			
		 Calls available to 3rd Party User as well as the Committer 
		 (ps: Committer has given Ref ID to the 3rd Part User)
		 
		 1. Get Message which is stored in Encrypted Format.
                    (ps: Use Ref ID 0, that we received in previous curl call)
                    Command --> curl http://127.0.0.1:5000/getMessageOnly/0
                    Output --> Ç<95>«×åÜã<85>ÅÒäå
                 
                 2. Get Complete Message Data stored in Database
                    Command --> curl http://127.0.0.1:5000/getMessageData/0
                    Output --> 0['Ç\x95«×åÜã\x85ÅÒäåÔ\x9b', 'Mon Apr 17 08:55:24 2017', 'įöĞĿōĽŖíĭĳŗōļü']
		
		 3. Get time when the message was posted.
		    Command --> curl http://127.0.0.1:5000/getTimePosted/0
		    Output --> Mon Apr 17 08:55:24 2017
	
		 4. Verify Data Integrity of the Message.
		    Command --> curl http://127.0.0.1:5000/verifyDataIntegrity/0
		    Output --> Data integrity verification successful for RefId: 0
		
		 5. Once the Message has been revealed by the Committer,
		    3rd Party User can call getMessageOnly again to see ther evealed data
		    Command --> curl http://127.0.0.1:5000/getMessageOnly/0
		    Output --> b'Hello World'



AUTHOR and REFERENCE

Author: Richa Mehta

Pre-commitment Scheme Reference:
https://en.wikipedia.org/wiki/Commitment_scheme
https://www.youtube.com/watch?v=bc8xcT0SN0g&t=54s

Encoding and Decoding of the Messages:
http://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password


