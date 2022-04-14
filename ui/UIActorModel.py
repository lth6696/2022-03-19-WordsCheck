import sys
import logging

from PyQt5.QtWidgets import *

from src.actor.ActorModel import Actor
from src.message.MsgModel import Message
from ui.UIFunction import UIFunctionImplement


class UIActorImplement(Actor):
    def __init__(self):
        super(UIActorImplement, self).__init__()

        self.windo = None

    def run(self):
        while True:
            msg = self.recv()
            # print(msg.__dict__)
            if not isinstance(msg, Message):
                continue
            logging.info('UIActorImplement - run - Message info {}'.format(msg.__dict__))
            if msg.recv != 'ui':
                continue
            try:
                getattr(self, msg.func)(**msg.args)
            except:
                logging.error('TransActorImplement - run - Request method {} not exist or arguments {} wrong.'
                              .format(msg.func, msg.args))

    def execute_ui(self, words, database_handler, translate_handler, pronounce_handler):
        app = QApplication(sys.argv)
        self.windo = UIFunctionImplement(words, database_handler, translate_handler, pronounce_handler)
        self.windo.show()
        sys.exit(app.exec_())

    def _show_text(self, text):
        self.windo._translate(text)

    def _add_wrong_words(self, words):
        try:
            self.windo.words += words
            logging.info('UIActorImplement - _add_wrong_words - Add wrong words.')
        except:
            logging.error('UIActorImplement - _add_wrong_words - Failed to add wrong words.')