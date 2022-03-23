import os
import sys
import random
import threading
import logging
import logging.config
import time
import inspect
import ctypes

from PyQt5.QtWidgets import *

import preprocess
import pronounce
import translate
from ui import mainwindow


TEMP_FILE = './temp'
DOCX_FILE = '../docx/24-28.docx'
WRONG_FILE = '../docx/wrong.csv'


class MainWdo(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super(MainWdo, self).__init__()
        self.setupUi(self)
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        logging.info('MainWdo - Program started.')

        self.setWindowTitle('单词检查程序')

        self.pron = self._set_audio_source()
        self.tran = translate.impl.TranslateImplement()
        self.ppi = preprocess.impl.PreProcessImplement()
        self.words = self._get_words()
        self.word = ''
        self.sample = [i for i in range(len(self.words))]
        self.wrong_answer = []
        self.correct_answer = -1
        self.threading = []

        self._set_sender()

    def _set_sender(self):
        self.PBCorrect.clicked.connect(self._correct)
        self.PBWrong.clicked.connect(self._wrong)
        self.PBReplay.clicked.connect(self._player)
        self.PBSpell.clicked.connect(self._show_spell_only)
        self.PBTranslate.clicked.connect(self._translate)
        self.PBExit.clicked.connect(self._exit)

        self.RBGoogle.toggled.connect(self._set_audio_source)
        self.RBBaidu.toggled.connect(self._set_audio_source)
        self.RBDeepL.toggled.connect(self._set_audio_source)
        self.RBYouDao.toggled.connect(self._set_audio_source)
        logging.info('MainWdo - Initialise the connection.')

    def _get_words(self):
        words = self.ppi.run(DOCX_FILE, WRONG_FILE)
        logging.info('MainWdo - Successfully acquire a set of words.')
        return words

    def _correct(self):
        if self.word == '' and self.correct_answer > -1:
            logging.error('MainWdo - The word can not be answered correctly.')
            return False
        self.correct_answer += 1
        logging.info('MainWdo - The number of correct answer is {}.'.format(self.correct_answer))
        self._cal_grade()
        # self._kill_threads()
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
        # self._kill_threads()
        self._next()

    def _player(self):
        if self.word == '':
            logging.error('MainWdo - There is no word.')
            return None
        self.pron.set_word(self.word)
        self.pron.set_accent(False)
        self.pron.play()
        logging.info('MainWdo - The word \'{}\' has been played.'.format(self.word))

    def _show_spell_only(self):
        if self.word == '':
            logging.error('MainWdo - There is no word.')
            return None
        self.TBShow.clear()
        self.TBShow.append(self.word)
        logging.info('MainWdo - The spell of \'{}\' has been showed in the QTextBrowser'.format(self.word))

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

    def _set_audio_source(self):
        if self.RBGoogle.isChecked():
            self.pron = pronounce.impl.GoogleImplement()
        elif self.RBBaidu.isChecked():
            pass
        elif self.RBDeepL.isChecked():
            pass
        elif self.RBYouDao.isChecked():
            self.pron = pronounce.impl.YouDaoImplement()
        else:
            self.pron = None
            logging.error('MainWdo - No QRadioButton is checked.')
        return self.pron

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

    def _exit(self):
        # for i in os.listdir(TEMP_FILE):
        #     file = TEMP_FILE + '/' + i
        #     os.remove(file)
        self._save_wrong_words()
        # self._kill_threads()
        self.close()
        logging.info('MainWdo - The program exited and all temp files deleted.')

    def _set_timer(self):
        def run():
            self._player()
            time.sleep(3)
            self._player()
            time.sleep(4)
        t = threading.Thread(target=run)
        self.threading.append(t)
        t.start()

    def _cal_grade(self):
        checked_words = len(self.wrong_answer) + int(self.correct_answer)
        if not checked_words:
            logging.error('MainWdo - Already checked answer is {}.'.format(checked_words))
            return False
        grade = self.correct_answer / checked_words * 100
        self.TBGrade.clear()
        self.TBGrade.append('Your score is {:.2f} in {}/{} words.'.format(grade, checked_words, len(self.words)))
        logging.info('MainWdo - Score updated to {:2f}.'.format(grade))

    def _save_wrong_words(self):
        if not self.wrong_answer:
            logging.error('MainWdo - You answer is all correct.')
            return False
        self.ppi.save(self.wrong_answer, WRONG_FILE)

    def _async_raise(self, tid, exctype):
        """Raises an exception in the threads with id tid"""
        if not inspect.isclass(exctype):
            logging.error('MainWdo - Only types can be raised (not instances)')
            raise TypeError("Only types can be raised (not instances)")
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
        if res == 0:
            logging.error('MainWdo - Invalid thread id.')
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            logging.error('MainWdo - PyThreadState_SetAsyncExc failed.')
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def _stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)

    def _kill_threads(self):
        for t in self.threading:
            self._stop_thread(t)
        self.threading = []
        logging.info('MainWdo - All threads are deleted.')


def main():
    app = QApplication(sys.argv)
    wdo = MainWdo()
    wdo.show()
    sys.exit(app.exec_())


def download_all_words_audio():
    ppi = preprocess.impl.PreProcessImplement()
    pron = pronounce.impl.GoogleImplement()
    words = ppi.run(DOCX_FILE, WRONG_FILE)
    for word in words:
        pron.set_word(word)
        pron.set_accent(True)
        pron.play()


if __name__ == '__main__':
    logging.config.fileConfig('config/config.ini')
    # main()
    download_all_words_audio()
    # todo 删除词根
    # todo 加入计时天数
