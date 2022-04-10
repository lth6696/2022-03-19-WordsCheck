import sys
import logging

from PyQt5.QtWidgets import *

from src.actor.ActorModel import Actor
from ui.UIFunction import UIFunctionImplement


class UIActorImplement(Actor):
    def __init__(self, words, database_handler, translate_handler, pronounce_handler):
        super(UIActorImplement, self).__init__()

        self.__execute_ui(words, database_handler, translate_handler, pronounce_handler)

    def run(self):
        while True:
            msg = self.recv()

    def __execute_ui(self, *args):
        app = QApplication(sys.argv)
        windo = UIFunctionImplement(*args)
        windo.show()
        sys.exit(app.exec_())