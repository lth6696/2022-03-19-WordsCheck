import logging

from src.message.MsgModel import Message
from src.actor.ActorModel import Actor
from src.translate.TransInterface import YouDaoTranslateImplement, OxfordTranslateImplement


class TransActorImplement(Actor):
    def __init__(self):
        super(TransActorImplement, self).__init__()

        self.trans = YouDaoTranslateImplement()

    def run(self):
        while True:
            msg = self.recv()
            if not isinstance(msg, Message):
                continue
            logging.info('TransActorImplement - run - Message info {}'.format(msg.__dict__))
            if msg.recv != 'translate':
                continue
            try:
                getattr(self, msg.func)(**msg.args)
            except:
                logging.error('TransActorImplement - run - Request method {} not exist or arguments {} wrong.'
                              .format(msg.func, msg.args))

    def translate(self, word, handler):
        self.trans.set_word(word)
        meanings = self.trans.paraphrase()
        for m in meanings:
            handler.append(m)
        logging.info('TransActorImplement - translate - The translation of \'{}\' has been showed in the QTextBrowser'.
                     format(word))
