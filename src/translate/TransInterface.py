import requests
import logging
import json

import bs4
import enchant


class TranslateImplement(object):
    def __init__(self, proxies: dict = None):
        self.word = ''
        self.enchant = enchant.Dict("en_US")
        self.proxies = proxies

    def set_word(self, word: str):
        if self._is_word(word):
            self.word = word
            logging.info('TranslateImplement - set_word - The word has been set to \'{}\''.format(self.word))
        else:
            logging.error('TranslateImplement - set_word - Check input spelling of {}.'.format(word))

    def get_word(self):
        return self.word

    def paraphrase(self):
        pass

    def _is_word(self, word):
        return self.enchant.check(word)


class YouDaoTranslateImplement(TranslateImplement):
    def __init__(self, proxies: dict = None):
        super(YouDaoTranslateImplement, self).__init__(proxies)
        logging.info('YouDaoTranslateImplement - Initialize the module of YouDaoTranslateImplement.')

    def _get_url(self):
        url = "https://dict.youdao.com/w/eng/" + str(self.word) + "/#keyfrom=dict2.index"
        logging.info('YouDaoTranslateImplement - Get the url {}'.format(url))
        return url

    def _soup(self, url):
        if not url:
            logging.error('YouDaoTranslateImplement - Incorrect url {}'.format(url))
            raise Exception('Incorrect url {}'.format(url))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv: 34.0 Gecko/20100101 Firefox/34.0'
        }
        response = requests.get(url, headers, proxies=self.proxies)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        logging.info('YouDaoTranslateImplement - The url has been parsed as Beautiful Soup.')
        return soup

    def paraphrase(self):
        url = self._get_url()
        soup = self._soup(url)
        trans_container = soup.find(name='div', attrs={'class': 'trans-container'})
        meanings = []
        tags = list(trans_container.children)[1]
        for li in tags.children:
            if type(li) == bs4.element.Tag:
                meanings.append(li.contents[0])
        logging.info('YouDaoTranslateImplement - The meaning of \'{}\' is obtained.'.format(self.word))
        return meanings


class OxfordTranslateImplement(TranslateImplement):
    def __init__(self, proxies: dict = None):
        super(OxfordTranslateImplement, self).__init__(proxies)
        logging.info('OxfordTranslateImplement - Initialize the module of OxfordTranslateImplement.')

        # The following attributions need to apply to the oxford official website.
        # The website is https://developer.oxforddictionaries.com/
        self.app_id = '0d976900'
        self.app_key = '77e065b0d619272e62408e8222113ff1'
        self.lang = "en-gb"

    def paraphrase(self):
        headers = {
            'app_id': self.app_id,
            'app_key': self.app_key
        }
        url = self._get_url()
        response = requests.get(url, headers=headers, timeout=1000, proxies=self.proxies)
        # 使用json()方法，将response对象，转为列表/字典
        content = response.json()
        """
        id: 单词
        metadata
        results
            - id: 单词
            - language
            - lexicalEntries: 词条
                - entries
                    - senses
                        - id
                        - translations
                - language
                - lexicalCategory
                    - id: 名词/动词...
                    - text: 名词/动词...
                - text: 单词
            - type: "headword"
            - word: 单词
        word: 单词
        """
        meanings = []
        for lexicalEntries in content['results'][0]['lexicalEntries']:
            tempType = []
            tempTrans = []
            type_ = lexicalEntries['lexicalCategory']['id']
            tempType.append(self._abbreviation(type_))
            for entries in lexicalEntries['entries']:
                for senses in entries['senses']:
                    for trans in senses['translations']:
                        tempTrans.append(trans['text'])
            tempType.append(', '.join(tempTrans))
            meanings.append(' '.join(tempType))
        logging.info('OxfordTranslateImplement - The meaning of \'{}\' is obtained.'.format(self.word))
        return meanings

    def _get_url(self):
        if self.word:
            url = "https://od-api.oxforddictionaries.com/api/v2/translations/en/zh/{}" \
                  "?strictMatch=false&fields=translations".format(self.word)
            logging.info('OxfordTranslateImplement - Get the url {}'.format(url))
        else:
            url = ''
        return url

    def _abbreviation(self, type_: str):
        if type_ == 'noun':
            type_ = 'n.'
        elif type_ == 'verb':
            type_ = 'v.'
        elif type_ == 'adjective':
            type_ = 'adj.'
        elif type_ == 'adverb':
            type_ = 'adv.'
        elif type_ == 'preposition':
            type_ = 'prep.'
        else:
            pass
        return type_
