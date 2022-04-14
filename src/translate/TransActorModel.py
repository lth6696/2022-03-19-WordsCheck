import logging

from src.message.MsgModel import Message
from src.actor.ActorModel import Actor
from src.translate.TransInterface import YouDaoTranslateImplement, OxfordTranslateImplement


class TransActorImplement(Actor):
    def __init__(self, ui_handler):
        super(TransActorImplement, self).__init__()

        self.trans = OxfordTranslateImplement()
        self.userinterfacer = ui_handler

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

    def translate(self, word):
        self.trans.set_word(word)
        meanings = self.trans.paraphrase()
        self.userinterfacer.send(Message('translate', 'ui', '_show_text', {'text': meanings}))
        logging.info('TransActorImplement - translate - The translation of \'{}\' has been send to UI'.format(word))
