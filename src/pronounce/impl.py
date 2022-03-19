import logging
import os
import urllib.request
from playsound import playsound

from .api import YouDao


class YouDaoImplement(YouDao):
    def __init__(self):
        YouDao.__init__(self)
        logging.info('YouDaoImplement - Initialize the module of YouDaoImplement.')
        self.type = self.set_accent()
        self.word = self.set_word()

    def set_accent(self, type :bool=True):
        if type:
            accent = "US"    # 美音
        else:
            accent = "EN"    # 英音
        logging.info('YouDaoImplement - The accent is set to {}.'.format(accent))
        return accent

    def get_accent(self):
        return self.type

    def play(self):
        if not os.path.exists('./temp'):
            logging.info('YouDaoImplement - Create a new directory in path {}.'.format('./temp'))
        temp = './temp/'+str(self.word)+'.mp3'
        url = self._get_url()
        urllib.request.urlretrieve(url, temp)
        logging.info('YouDaoImplement - The audio of \'{}\' is saved to {}'.format(self.word, './temp'))
        playsound(temp)
        return None

    def set_word(self, word='abandon'):
        if not word:
            logging.error('No word.')
            raise Exception('No word.')
        self.word = word
        logging.info('YouDaoImplement - The word has been set to \'{}\''.format(self.word))
        return str(word)

    def _get_url(self):
        accent = 0 if self.type == "US" else 1
        url = r'http://dict.youdao.com/dictvoice?type='+str(accent)+r'&audio='+self.word
        logging.info('YouDaoImplement - Successfully get the url {}'.format(url))
        return url
