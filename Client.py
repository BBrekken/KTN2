# -*- coding: utf-8 -*-
import socket
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.server_port = server_port

        #The valid requests a user can type in.
        self.validInputs = {
            "login": self.login(self.inContent),
            "logout": self.logout(),
            "msg": self.msg(self.inContent),
            "names": self.names(),
            "help": self.help()
        }

        # Users request
        self.inContent = ''
        self.request = {'request': None, 'content': None}

        #Creates a MessageParser object
        self.messageParser = MessageParser()


        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

        #Creates and starts MessageReceiver
        thread = MessageReceiver(client=self, connection=self.connection)
        thread.start()

        #Reads user input
        while True:
            inputData = input('Input: ').split()
            self.inContent = inputData[1]
            if inputData[0] in self.validInputs:
                self.request = self.validInputs[inputData[0]]
            else:
                print('This is not a valid request.')

    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.shutdown(socket.SHUT_RDWR)
        self.connection.close()

    def receive_message(self, message):
        # Parses a received message
        self.messageParser.parse(message)

    def send_payload(self):
        # Handles and sends payload to Server
        jsonRequsest = json.dumps(self.request)
        self.connection.sendall(jsonRequsest)

    # More methods may be needed!

    # Method for login
    def login(self, username):
        if len(username) < 1:
            print("Please type in username after 'login'.")
        else:
            self.request['content'] = username
            self.send_payload()

    # Method for logout
    def logout(self):
        self.send_payload()

    # Method for sending message
    def msg(self, message):
        if len(message) < 1:
            print("Please type in your message after 'msg'.")
        else:
            self.request['content'] = message
            self.send_payload()

    # Method for getting all users
    def names(self):
        self.send_payload()

    # Method for getting help description
    def help(self):
        self.send_payload()


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
