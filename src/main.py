import logging.config
import sys

from PyQt5.QtWidgets import *

from src.dictionary.DictInterface import DictInterfaceImplement
from src.dictionary.DictActorModel import DictActorImplement
from src.pronounce.PronInterface import GoogleImplement
from src.pronounce.PronActorModel import PronActorImplement
from src.translate.TransActorModel import TransActorImplement
from src.message.MsgModel import Message
from ui.UIFunction import UIFunctionImplement

TEMP_FILE = './temp'
DOCX_FILE = '../docx/68-70.csv'
WRONG_FILE = '../docx/wrong.csv'
RANGE = '068070'


def download_all_words_audio(audio=True):
    dict_iface = DictInterfaceImplement()
    pron = GoogleImplement()
    words = dict_iface.run(DOCX_FILE, WRONG_FILE)
    if audio:
        for word in words:
            pron.set_word(word)
            pron.set_accent(True)
            pron.play(False)
    return words


if __name__ == '__main__':
    logging.config.fileConfig('config/config.ini')
    words = download_all_words_audio(False)

    threads = {}
    threads['database'] = DictActorImplement(name='words.db', table='checkwords')
    threads['pronounce'] = PronActorImplement()
    threads['translate'] = TransActorImplement()
    for key in threads:
        threads[key].start()

    threads['database'].send(Message('ui', 'database', 'insert', {'words': words, 'range': RANGE}))

    app = QApplication(sys.argv)
    windo = UIFunctionImplement(words, threads['database'], threads['translate'], threads['pronounce'])
    windo.show()
    sys.exit(app.exec_())