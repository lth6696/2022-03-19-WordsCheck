import logging

from src.actor.ActorModel import Actor
from src.message.MsgModel import Message
from src.pronounce.PronInterface import YouDaoImplement, GoogleImplement, OxfordImplement


class PronActorImplement(Actor):
    def __init__(self, proxies: dict = None):
        super(PronActorImplement, self).__init__()
        self.pron = YouDaoImplement()
        self.proxies = proxies

    def run(self):
        while True:
            msg = self.recv()
            if not isinstance(msg, Message):
                continue
            logging.info('PronActorImplement - run - Message info {}'.format(msg.__dict__))
            if msg.recv != 'pronounce':
                continue
            try:
                getattr(self, msg.func)(**msg.args)
            except:
                logging.error('PronActorImplement - run - Request method {} not exist or arguments {} wrong.'
                              .format(msg.func, msg.args))

    def set_source(self, name):
        if name == 'Google':
            self.pron = GoogleImplement()
            logging.info('PronActorImplement - set_source - Switch to source \'Google\'.')
        elif name == 'YouDao':
            self.pron = YouDaoImplement()
            logging.info('PronActorImplement - set_source - Switch to source \'YouDao\'.')
        elif name == 'Oxford':
            self.pron = OxfordImplement(proxies=self.proxies)
            logging.info('PronActorImplement - set_source - Switch to source \'Oxford\'.')
        else:
            logging.error('PronActorImplement - set_source - Source no found \'{}\'.'.format(name))

    def play(self, word):
        self.pron.set_word(word)
        self.pron.play()
