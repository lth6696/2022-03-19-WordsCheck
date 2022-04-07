import logging

import requests
import bs4
import logging

from src.translate.api import Translate


class TranslateImplement(Translate):
    def __init__(self):
        Translate.__init__(self)
        logging.info('TranslateImplement - Initialize the module of TranslateImplement.')
        self.word = self.set_word()

    def _get_url(self):
        url = "https://dict.youdao.com/w/eng/" + str(self.word) + "/#keyfrom=dict2.index"
        logging.info('TranslateImplement - Get the url {}'.format(url))
        return url

    def _soup(self, url):
        if not url:
            logging.error('TranslateImplement - Incorrect url {}'.format(url))
            raise Exception('Incorrect url {}'.format(url))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv: 34.0 Gecko/20100101 Firefox/34.0'
        }
        response = requests.get(url, headers)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        logging.info('TranslateImplement - The url has been parsed as Beautiful Soup.')
        return soup

    def set_word(self, word='abandon'):
        self.word = word
        logging.info('TranslateImplement - The word has been set to \'{}\''.format(self.word))
        return str(word)

    def paraphrase(self):
        url = self._get_url()
        soup = self._soup(url)
        trans_container = soup.find(name='div', attrs={'class': 'trans-container'})
        meanings = []
        tags = list(trans_container.children)[1]
        for li in tags.children:
            if type(li) == bs4.element.Tag:
                meanings.append(li.contents[0])
        logging.info('TranslateImplement - The meaning of \'{}\' is obtained.'.format(self.word))
        return meanings