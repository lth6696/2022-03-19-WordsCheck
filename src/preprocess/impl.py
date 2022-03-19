import docx2txt
import os
import re
import enchant
import csv
import logging

from .api import PreProcess


class PreProcessImplement(PreProcess):
    def __init__(self):
        PreProcess.__init__(self)
        logging.info('PreProcessImplement - Initialized a module of PreProcessImplement.')

    def read_docx(self, path=''):
        if path == '':
            path = '../docx/word.docx'
        if not os.path.exists(path):
            logging.error("PreProcessImplement - Can not find docx file in {}".format(path))
            raise Exception("Can not find docx file in {}".format(path))
        word_content = docx2txt.process(path)
        logging.info('PreProcessImplement - Successfully get the content of {}'.format(path))
        return word_content

    def find_words(self, text):
        text_without_symbol = re.compile("\w+").findall(text)
        dictionary = enchant.Dict("en_US")
        words = []
        for word in text_without_symbol:
            if len(word) > 4 and dictionary.check(word):
                words.append(str.lower(word))
            else:
                pass
        logging.info('PreProcessImplement - {} words has been checked out.'.format(len(words)))
        return words

    def save(self, words: list, path: str):
        if not words:
            logging.error('PreProcessImplement - There are no words need to save.')
            raise Exception('Empty words.')
        with open(path, 'w', newline='', encoding='utf-8') as f:
            file = csv.writer(f)
            file.writerow(words)
            logging.info('PreProcessImplement - Words saved in the {}'.format(path))
        return None

    def read(self, path: str):
        words = []
        with open(path) as f:
            file = csv.reader(f)
            for row in file:
                words += row
            logging.info('PreProcessImplement - Words have been read in memory.')
        return words