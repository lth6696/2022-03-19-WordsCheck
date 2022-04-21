import logging.config


from src.dictionary.DictInterface import DictInterfaceImplement
from src.dictionary.DictDataBase import DataBaseImplement
from src.dictionary.DictActorModel import DictActorImplement
from src.pronounce.PronInterface import GoogleImplement
from src.pronounce.PronActorModel import PronActorImplement
from src.translate.TransActorModel import TransActorImplement
from src.message.MsgModel import Message
from ui.UIActorModel import UIActorImplement

TEMP_FILE = './temp'
DOCX_FILE = '../docx/95-99.csv'
WRONG_FILE = '../docx/wrong.csv'
RANGE = '095'
PROXY = {'https': 'http://127.0.0.1:8889'}
# PROXY = None


def download_all_words_audio(audio=True):
    dict_iface = DictInterfaceImplement()
    pron = GoogleImplement()
    words = dict_iface.run(DOCX_FILE)
    if audio:
        for word in words:
            pron.set_word(word)
            pron.set_accent(True)
            pron.play(False)
    return words


def review_words():
    db = DataBaseImplement()
    db.database_connect('words.db')
    records = db.database_find_records('checkwords', columns=['word'], const={'level': ''})
    review_words = [word[0] for word in records]
    return review_words


if __name__ == '__main__':
    logging.config.fileConfig('config/config.ini')
    words = download_all_words_audio(False)
    # words = review_words()

    threads = {}
    threads['ui'] = UIActorImplement()
    threads['database'] = DictActorImplement(name='words.db', table='checkwords', ui_handler=threads['ui'])
    threads['pronounce'] = PronActorImplement(proxies=PROXY)
    threads['translate'] = TransActorImplement(ui_handler=threads['ui'], proxies=PROXY)
    for key in threads:
        threads[key].start()

    threads['database'].send(Message('main', 'database', 'insert', {'words': words, 'range': RANGE}))
    threads['ui'].execute_ui(words, threads['database'], threads['translate'], threads['pronounce'])