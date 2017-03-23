# -*- coding: utf-8 -*-
import socketserver
import json
import re
import datetime
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    usernames = []
    connectetClients = []
    connections = []
    msgLog = []
    helpText = "Type: login <username> to logg in \n " \
               "Type: logout to log out \n " \
               "Type: msg <you message> to send a message \n " \
               "Type: names to see all people in the chat \n " \
               "Type: history to all messages sent in the chat \n "
    response = {
        'timestamp': '',
        'sender': '',
        'response': '',
        'content': ''
    }

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.username = ''

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            data = json.loads(received_string)
            request = data['requst']
            if request == 'login':
                if self in self.connectetClients:
                    self.sendResponse('', 'error', 'You are already logged in.')
                else:
                    self.login(data['content'])
            elif request == 'help':
                self.help()
            elif request == 'logout':
                self.logout()
            elif request == 'history':
                self.history()
            elif request == 'msg':
                self.message(data['content'])
            elif request == 'names':
                self.names()

    def getTimestamp(self):
        return str(datetime.datetime.now())

    def sendResponse(self, sender, response, content):
        self.request['timestamps'] = self.getTimestamp()
        self.request['sernder'] = sender
        self.request['response'] = response
        self.request['content'] = content
        self.sendMessage(self.response)

    def sendMessage(self, data):
        self.connection.sendall(json.dumps(data).encode())

    def login(self, username):
        # TODO: add errors
        if (not re.match(r'^[A-Za-z0-9]+$', username)):
            self.sendResponse('', 'error', 'Invalid username.')
        elif username in self.usernames:
            self.sendResponse('', 'error', 'This user is allready logged in.')
        else:
            self.connectetClients.append(self)
            self.usernames.append(username)
            self.sendResponse('', 'info', 'You are now logged in as ' + username)

    def logout(self):
        self.connectetClients.remove(self)
        self.usernames.remove(self.username)
        self.sendResponse('', 'info', 'You are now logged out')

    def message(self, message):
        if len(message) < 1:
            self.sendResponse('', 'error', 'Message empty.')
        else:
            msgInfo = {'timestamps': self.getTimestamp(), 'sender': self.username, 'response': 'history', 'content': message}
            self.msgLog.append(msgInfo)
            for client in self.connectetClients:
                client.sendResponse(self.username, 'message', message)

    def names(self):
        names = ' '.join(name for name in self.usernames)
        self.sendResponse('', 'info', names)

    def help(self):
        self.sendResponse('', 'info', self.helpText)

    def history(self):
        history = '\n'.join(msg for msg in self.msgLog)
        self.sendResponse('', 'info', history)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print ('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
