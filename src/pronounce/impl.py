import logging
import os
import urllib.request
from playsound import playsound
from gtts import gTTS

from .api import Pronounce


class YouDaoImplement(Pronounce):
    def __init__(self):
        Pronounce.__init__(self)
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
        path = './temp'
        if not os.path.exists(path):
            logging.info('YouDaoImplement - Create a new directory in path {}.'.format(path))
            os.mkdir(path)
        temp = path + '/' + str(self.word) + '.mp3'
        if not os.path.exists(temp):
            url = self._get_url()
            urllib.request.urlretrieve(url, temp)
            logging.info('YouDaoImplement - The audio of \'{}\' is saved to {}'.format(self.word, path))
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


class GoogleImplement(Pronounce):
    def __init__(self):
        Pronounce.__init__(self)
        logging.info('GoogleImplement - Initialize the module of GoogleImplement.')
        self.type = self.set_accent()
        self.word = self.set_word()

    def set_accent(self, type: bool = True):
        if type:
            # default is US
            accent = {'lang': 'en', 'tld': 'com'}
        else:
            # type is UK
            accent = {'lang': 'en', 'tld': 'co.uk'}
        return accent

    def get_accent(self):
        return self.type

    def set_word(self, word='abandon'):
        if not word:
            logging.error('No word.')
            raise Exception('No word.')
        self.word = word
        logging.info('GoogleImplement - The word has been set to \'{}\''.format(self.word))
        return str(word)

    def get_word(self):
        return self.word

    def play(self):
        path = './temp'
        if not os.path.exists(path):
            logging.info('GoogleImplement - Create a new directory in path {}.'.format(path))
            os.mkdir(path)
        temp = path + '/' + str(self.word) + '.mp3'
        if not os.path.exists(temp):
            tts = gTTS(text=self.word, **self.type)
            tts.save(temp)
            logging.info('GoogleImplement - The audio of \'{}\' has been saved.'.format(self.word))
        # playsound(temp)
        return None
