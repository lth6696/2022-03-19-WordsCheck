import os
import sys
import random
import threading
import logging
import logging.config
import time

from PyQt5.QtWidgets import *

import preprocess
import pronounce
import translate
from ui import mainwindow


TEMP_FILE = './temp'
DOCX_FILE = '../docx/14-18.docx'


class MainWdo(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super(MainWdo, self).__init__()
        self.setupUi(self)
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        logging.info('MainWdo - Program started.')

        self.setWindowTitle('单词检查程序')

        self.pron = pronounce.impl.YouDaoImplement()
        # self.pron = pronounce.impl.GoogleImplement()
        self.tran = translate.impl.TranslateImplement()
        self.words = self._get_words()
        self.word = ''
        self.sample = [i for i in range(len(self.words))]
        self.wrong_answer = []
        self.correct_answer = -1

        self._set_sender()

    def _get_words(self):
        ppi = preprocess.impl.PreProcessImplement()
        words = ppi.run(DOCX_FILE)
        logging.info('MainWdo - Successfully acquire a set of words.')
        return words

    def _set_sender(self):
        self.PBCorrect.clicked.connect(self._correct)
        self.PBWrong.clicked.connect(self._wrong)
        self.PBReplay.clicked.connect(self._player)
        self.PBTranslate.clicked.connect(self._translate)
        self.PBExit.clicked.connect(self._exit)
        logging.info('MainWdo - Initialise the connection.')

    def _next(self):
        if not self.words:
            logging.error('MainWdo - The set of words does not exist.')
            raise Exception('The set of words does not exist.')
        index = random.sample(self.sample, 1)
        self.sample.remove(index[0])
        self.word = self.words[index[0]]
        self.TBShow.clear()
        self.TBShow.setText("Please recite the meaning of the words according to the audio.")
        logging.info('MainWdo - The word \'{}\' has been selected.'.format(self.word))
        self._set_timer()

    def _correct(self):
        if self.word == '' and self.correct_answer > -1:
            logging.error('MainWdo - The word can not be answered correctly.')
            return False
        self.correct_answer += 1
        logging.info('MainWdo - The number of correct answer is {}.'.format(self.correct_answer))
        self._cal_grade()
        self._next()

    def _wrong(self):
        if self.word == '':
            logging.info('MainWdo - There is no word.')
            return False
        self.wrong_answer.append(self.word)
        logging.info('MainWdo - The number of wrong answer is {}.'.format(len(self.wrong_answer)))
        index = self.words.index(self.word)
        self.sample.append(index)
        self._cal_grade()
        self._next()

    def _player(self):
        if self.word == '':
            logging.error('MainWdo - There is no word.')
            return None
        self.pron.set_word(self.word)
        self.pron.set_accent(False)
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

    def _set_timer(self):
        def run():
            self._player()
            time.sleep(3)
            self._player()
            time.sleep(4)
        t = threading.Thread(target=run)
        t.start()

    def _cal_grade(self):
        checked_words = len(self.wrong_answer) + int(self.correct_answer)
        if not checked_words:
            logging.error('MainWdo - Already checked answer is {}.'.format(checked_words))
            return False
        grade = self.correct_answer / checked_words * 100
        self.TBGrade.clear()
        self.TBGrade.append('Your score is {:.2f} in {} words.'.format(grade, checked_words))
        logging.info('MainWdo - Score updated to {:2f}.'.format(grade))


def main():
    app = QApplication(sys.argv)
    wdo = MainWdo()
    wdo.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    logging.config.fileConfig('config/config.ini')
    main()

    # todo 加入之前错误的单词和部分正确的单词