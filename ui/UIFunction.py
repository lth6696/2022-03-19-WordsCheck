import logging
import random
import pdb

from PyQt5.QtWidgets import *

from ui.MainWindow import Ui_MainWindow
from src.message.MsgModel import Message


class UIFunctionImplement(QMainWindow, Ui_MainWindow):
    def __init__(self, words: list, database_handler, translate_handler, pronounce_handler):
        super(UIFunctionImplement, self).__init__()
        self.setupUi(self)
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        logging.info('MainWdUIFunctionImplement - Initialize the ui function.')

        self.setWindowTitle('Check Words')

        self.translator = translate_handler
        self.databaser = database_handler
        self.pronouncer = pronounce_handler

        self.words = words
        self.word = ''
        self.grade = {'right': 0, 'wrong': 0}
        self.threading = []
        self.is_first_boot = True

        self._set_sender()
        self._set_source()
        self._get_wrong_words()

    def _set_sender(self):
        self.PBCorrect.clicked.connect(self._correct)
        self.PBWrong.clicked.connect(self._wrong)
        self.PBReplay.clicked.connect(self._player)
        self.PBSpell.clicked.connect(self._show_spell_only)
        self.PBTranslate.clicked.connect(self._translate)
        self.PBExit.clicked.connect(self._exit)

        self.RBGoogle.toggled.connect(self._set_source)
        self.RBOxford.toggled.connect(self._set_source)
        self.RBDeepL.toggled.connect(self._set_source)
        self.RBYouDao.toggled.connect(self._set_source)
        logging.info('UIFunctionImplement - Initialise the connection.')

    def _correct(self):
        if not self.word:
            if self.is_first_boot:
                self.is_first_boot = False
                self._next()
                self._player()
            else:
                logging.error('UIFunctionImplement - _correct - A word must be set.')
        else:
            self.grade['right'] += 1
            self.databaser.send(Message('ui', 'database', 'update', {'word': self.word, 'level': 'correct'}))
            self.words.remove(self.word)
            self._cal_grade()
            self._next()
            self._player()
            logging.info('UIFunctionImplement - _correct - The number of correct answer is {}.'.format(self.grade['right']))

    def _wrong(self):
        if not self.word:
            if self.is_first_boot:
                self.is_first_boot = False
                self._next()
                self._player()
            else:
                logging.error('UIFunctionImplement - _wrong - A word must be set.')
        else:
            self.grade['wrong'] += 1
            self.databaser.send(Message('ui', 'database', 'update', {'word': self.word, 'level': 'wrong'}))
            self.words.remove(self.word)
            self._cal_grade()
            self._next()
            self._player()
            logging.info('UIFunctionImplement - _wrong - The number of wrong answer is {}.'.format(self.grade['wrong']))

    def _player(self):
        if not self.word:
            logging.error('UIFunctionImplement - _player - A word must be set.')
        else:
            self.pronouncer.send(Message('ui', 'pronounce', 'play', {'word': self.word}))
            logging.info('UIFunctionImplement - _player - The word \'{}\' has been played.'.format(self.word))

    def _show_spell_only(self):
        if not self.word:
            logging.error('UIFunctionImplement - _show_spell_only - A word must be set.')
        else:
            self.TBShow.clear()
            self.TBShow.append(self.word)
            logging.info('UIFunctionImplement - _show_spell_only - '
                         'The spell of \'{}\' has been showed in the QTextBrowser'.format(self.word))

    def _translate(self, meanings: list = None):
        if not self.word:
            logging.error('UIFunctionImplement - _translate - A word must be set.')
        elif meanings:
            for text in meanings:
                self.TBShow.append(text)
        else:
            self.TBShow.clear()
            self.TBShow.append(self.word)
            self.translator.send(Message('ui', 'translate', 'translate', {'word': self.word}))

    def _set_source(self):
        if self.RBGoogle.isChecked():
            self.pronouncer.send(Message('ui', 'pronounce', 'set_source', {'name': 'Google'}))
            self.translator.send(Message('ui', 'translate', 'set_source', {'name': 'Google'}))
        elif self.RBOxford.isChecked():
            self.pronouncer.send(Message('ui', 'pronounce', 'set_source', {'name': 'Oxford'}))
            self.translator.send(Message('ui', 'translate', 'set_source', {'name': 'Oxford'}))
        elif self.RBDeepL.isChecked():
            self.pronouncer.send(Message('ui', 'pronounce', 'set_source', {'name': 'DeepL'}))
            self.translator.send(Message('ui', 'translate', 'set_source', {'name': 'DeepL'}))
        elif self.RBYouDao.isChecked():
            self.pronouncer.send(Message('ui', 'pronounce', 'set_source', {'name': 'YouDao'}))
            self.translator.send(Message('ui', 'translate', 'set_source', {'name': 'YouDao'}))
        else:
            logging.error('UIFunctionImplement - _set_audio_source - No QRadioButton is checked.')

    def _next(self):
        if not self.words:
            logging.error('UIFunctionImplement - _next - The set of words does not exist.')
        else:
            self.word = random.choice(self.words)
            self.TBShow.clear()
            self.TBShow.setText("Please recite the meaning of the words according to the audio.")
            logging.info('UIFunctionImplement - _next - The word \'{}\' has been selected.'.format(self.word))

    def _exit(self):
        self.close()
        logging.info('UIFunctionImplement - _exit - UI exited.')

    def _cal_grade(self):
        checked_words = self.grade['right'] + self.grade['wrong']
        if not checked_words:
            logging.error('UIFunctionImplement - _cal_grade - Already checked answer is {}.'.format(checked_words))
        else:
            grade = self.grade['right'] / checked_words * 100
            self.TBGrade.clear()
            self.TBGrade.append('Your score is {:.2f} within {} words and {} remaining.'.format(grade,
                                                                                                checked_words,
                                                                                                len(self.words)))
            logging.info('UIFunctionImplement - _cal_grade - Score updated to {:2f}.'.format(grade))

    def _get_wrong_words(self):
        self.databaser.send(Message('ui', 'database', 'find_wrong_words', {}))
