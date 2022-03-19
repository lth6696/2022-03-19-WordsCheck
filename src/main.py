import os
import sys
import random
import threading
import logging
import logging.config
from PyQt5.QtWidgets import *

import preprocess
import pronounce
import translate
from ui import mainwindow


TEMP_FILE = './temp'
DOCX_FILE = '../docx/word.docx'


class MainWdo(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super(MainWdo, self).__init__()
        self.setupUi(self)
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        logging.info('MainWdo - Program started.')

        self.setWindowTitle('单词检查程序')

        self.pron = pronounce.impl.YouDaoImplement()
        self.tran = translate.impl.TranslateImplement()
        self.words = self._get_words()
        self.word = ''

        self._set_sender()

    def _get_words(self):
        ppi = preprocess.impl.PreProcessImplement()
        content = ppi.read_docx(DOCX_FILE)
        words = ppi.find_words(content)
        # ppi.save(words, 'w.csv')
        logging.info('MainWdo - Successfully acquire a set of words.')
        return words

    def _set_sender(self):
        self.PBNext.clicked.connect(self._next)
        self.PBPlayer.clicked.connect(self._player)
        self.PBTranslate.clicked.connect(self._translate)
        self.PBExit.clicked.connect(self._exit)
        logging.info('MainWdo - Initialise the connection.')

    def _next(self):
        if not self.words:
            logging.error('MainWdo - The set of words does not exist.')
            raise Exception('The set of words does not exist.')
        index = random.randint(0, len(self.words)-1)
        self.word = self.words[index]
        self.TBShow.clear()
        self.TBShow.setText("Please recite the meaning of the words according to the audio.")
        logging.info('MainWdo - The word \'{}\' has been selected.'.format(self.word))
        self._player()

    def _player(self):
        if self.word == '':
            logging.error('MainWdo - There is no word.')
            return None
        self.pron.set_word(self.word)
        t = threading.Thread(target=self.pron.play)
        t.start()
        logging.info('MainWdo - The word \'{}\' has been played.'.format(self.word))

    def _translate(self):
        if self.word == '':
            logging.error('MainWdo - There is no word.')
            return None
        self.tran.set_word(self.word)
        meanings = self.tran.paraphrase()
        self.TBShow.clear()
        self.TBShow.append(self.word)
        for m in meanings:
            self.TBShow.append(m)
        logging.info('MainWdo - The translation of \'{}\' has been showed in the QTextBrowser'.format(self.word))

    def _exit(self):
        self.close()
        for i in os.listdir(TEMP_FILE):
            file = TEMP_FILE + '/' + i
            os.remove(file)
        logging.info('MainWdo - The program exited and all temp files deleted.')


def main():
    app = QApplication(sys.argv)
    wdo = MainWdo()
    wdo.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    logging.config.fileConfig('config/config.ini')
    main()