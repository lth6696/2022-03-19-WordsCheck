import logging
import os

import urllib.request
import requests
from playsound import playsound
from gtts import gTTS


class YouDaoImplement(object):
    def __init__(self):
        logging.info('YouDaoImplement - Initialize the module of YouDaoImplement.')
        self.accent = self.set_accent()
        self.word = self.set_word()

    def set_accent(self, type: bool = True):
        if type:
            accent = "US"  # 美音
        else:
            accent = "EN"  # 英音
        logging.info('YouDaoImplement - The accent is set to {}.'.format(accent))
        return accent

    def get_accent(self):
        return self.accent

    def play(self, play=True):
        path = './temp'
        if not os.path.exists(path):
            logging.info('YouDaoImplement - Create a new directory in path {}.'.format(path))
            os.mkdir(path)
        temp = path + '/' + str(self.word) + '_you' + '_{}.mp3'.format(self.accent)
        if not os.path.exists(temp):
            url = self._get_url()
            urllib.request.urlretrieve(url, temp)
            logging.info('YouDaoImplement - The audio of \'{}\' is saved to {}'.format(self.word, path))
        if play:
            playsound(temp)
        return None

    def set_word(self, word='abandon'):
        if not word:
            logging.error('YouDaoImplement - No word.')
            raise Exception('No word.')
        self.word = word
        logging.info('YouDaoImplement - The word has been set to \'{}\''.format(self.word))
        return str(word)

    def _get_url(self):
        accent = 0 if self.accent == "US" else 1
        url = r'http://dict.youdao.com/dictvoice?type=' + str(accent) + r'&audio=' + self.word
        logging.info('YouDaoImplement - Successfully get the url {}'.format(url))
        return url


class GoogleImplement(object):
    def __init__(self):
        logging.info('GoogleImplement - Initialize the module of GoogleImplement.')
        self.accent = self.set_accent()
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
        return self.accent

    def set_word(self, word='abandon'):
        if not word:
            logging.error('GoogleImplement - No word.')
            raise Exception('No word.')
        self.word = word
        logging.info('GoogleImplement - The word has been set to \'{}\''.format(self.word))
        return str(word)

    def get_word(self):
        return self.word

    def play(self, play=True):
        path = './temp'
        if not os.path.exists(path):
            logging.info('GoogleImplement - Create a new directory in path {}.'.format(path))
            os.mkdir(path)
        temp = path + '/' + str(self.word) + '_goo' '_{}.mp3'.format(self.accent)
        if not os.path.exists(temp):
            tts = gTTS(text=self.word, **self.accent)
            tts.save(temp)
            logging.info('GoogleImplement - The audio of \'{}\' has been saved.'.format(self.word))
        if play:
            playsound(temp)
        return None


class OxfordImplement(object):
    def __init__(self, accent: str = 'us', proxies: dict = None):
        logging.info('OxfordImplement - Initialize the module of OxfordImplement.')
        # self.type = self.set_accent()
        self.word = self.set_word()
        self.accent = accent
        self.proxies = proxies

    def set_word(self, word='abandon'):
        if not word:
            logging.error('OxfordImplement - No word.')
            return ''
        else:
            self.word = word
            logging.info('OxfordImplement - The word has been set to \'{}\''.format(self.word))
            return str(word)

    def get_word(self):
        return self.word

    def set_accent(self, accent):
        if accent in ['uk', 'us']:
            self.accent = accent
            logging.info('OxfordImplement - set_accent - Accent has been set to \'{}\'.'.format(self.accent))
        else:
            logging.error('OxfordImplement - set_accent - Input wrong type of accent \'{}\''.format(accent))

    def get_accent(self):
        return self.accent

    def play(self, play=True):
        path = './temp'
        if not os.path.exists(path):
            logging.info('OxfordImplement - Create a new directory in path {}.'.format(path))
            os.mkdir(path)
        temp = path + '/' + str(self.word) + '_oxf' + '_{}.mp3'.format(self.accent)
        if not os.path.exists(temp):
            req = requests.get(self.__get_url(), proxies=self.proxies, timeout=1000)
            with open(temp, 'wb') as file:
                file.write(req.content)
                logging.info('OxfordImplement - The audio of \'{}\' has been saved.'.format(self.word))
        if play:
            playsound(temp)

    def __get_url(self):
        if self.accent == 'uk':
            url = "https://lex-audio.useremarkable.com/mp3/{}__gb_1.mp3".format(self.word)
        elif self.accent == 'us':
            url = "https://lex-audio.useremarkable.com/mp3/{}__us_1.mp3".format(self.word)
        else:
            url = ''
        return url
