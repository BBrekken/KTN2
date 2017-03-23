import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
	    # More key:values pairs are needed	
        }

    def parse(self, payload):
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            print('respones not valid')

    def parse_error(self, payload):
        print('Recived an error:')
        print(json.dump(payload, indent=3))

    def parse_info(self, payload):
        print('Recived info:')
        print(json.dump(payload, indent=3))

    # Include more methods for handling the different responses...
