# -*- coding: utf-8 -*-
import socketserver
import json

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
    connections = []
    helpText = ''
    response = {
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

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            
            # TODO: Add handling of received payload from client

    def sendResponse(self, data):
        self.connection.sendall(json.dumps(data))

    def login(self, username):
        # TODO: add errors
        if username in self.usernames:
            self.response['response'] = 'error'
            self.response['content'] = 'username already taken'
        else:
            self.usernames.append(username)
            self.response['response'] = 'info'
            self.response['content'] = 'now logged in as: ' + username

    def logout(self, username):
        # TODO: add errors
        if username in self.usernames:
            self.usernames.remove(username)
            self.response['response'] = 'info'
            self.response['content'] = 'now logged out'

    def msg(self, message):
        if len(message) < 1:
            self.response['response'] = 'error'
            self.response['content'] = 'you message had no content'
        else:
            self.response['response'] = 'info'
            self.response['content'] = 'message sent: ' + message
            for client in self.connections:
                client.sendResponse(self.request)

    def names(self):
        self.response['response'] = 'info'
        names = ''
        for user in self.usernames:
            names += user + ', '
        self.response['content'] = names
        self.sendResponse(self.response)

    def help(self):
        self.response['response'] = 'info'
        self.response['content'] = self.helpText
        self.sendResponse(self.response)


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
