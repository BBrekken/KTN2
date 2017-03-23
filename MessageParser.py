import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'history': self.parse_history,
            'msg': self.parse_msg
        }

    # Payload: {'timestamps: 'timestamp', 'sender': 'username', 'response': 'response', 'contetn':'content'}
    def parse(self, payload):
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            print('respones not valid')

    def parse_error(self, payload):
        print('Recived an error:')
        print(payload['content'] + '\n')

    def parse_info(self, payload):
        print('Recived info:' + payload['content'] + '\n')

    def parse_history(self, payload):
        print('History: ' + payload['timestmaps'] + ' ' + payload['sender'] + ' ' + payload['content'] + '\n')

    def parse_msg(self, payload):
        print('Message: ' + payload['timestmaps'] + ' ' + payload['sender'] + ' ' + payload['content'] + '\n')
