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

    def read_docx(self, path):
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
        with open(path, 'a', newline='', encoding='utf-8') as f:
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

    def read_wrong_file(self, path):
        if not os.path.exists(path):
            logging.error("PreProcessImplement - Can not find wrong file in {}".format(path))
            raise Exception("Can not find wrong file in {}".format(path))
        words = self.read(path)
        return words

    def run(self, path, wrong_file=''):
        csv_path = str(path).replace('.docx', '.csv')
        words = []
        if os.path.exists(csv_path):
            logging.info('PreProcessImplement - Find the last-save file {}.'.format(csv_path))
            words += self.read(csv_path)
        else:
            content = self.read_docx(path)
            words += self.find_words(content)
            self.save(words, csv_path)
        if os.path.exists(wrong_file):
            words += self.read_wrong_file(wrong_file)
        logging.info("PreProcessImplement - Totally load {} words this time.".format(len(words)))
        return words