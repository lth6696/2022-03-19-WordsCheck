

class Message(object):
    def __init__(self, send, recv, func, args):
        self.send = send
        self.recv = recv
        self.func = func
        self.args = args

    def initialize(self):
        pass