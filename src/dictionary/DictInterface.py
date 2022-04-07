import os
import re
import csv
import logging

import docx2txt
import enchant

from src.dictionary.DictDataBase import DataBaseImplement


class DictInterfaceImplement(object):
    def __init__(self):
        logging.info('DictInterfaceImplement - Initialized a module of DictInterfaceImplement.')
        self.enchant = enchant.Dict("en_US")

    def run(self, path, wrong_file=''):
        csv_path = str(path).replace('.docx', '.csv')
        words = []
        if os.path.exists(csv_path):
            logging.info('DictInterfaceImplement - Find the last-save file {}.'.format(csv_path))
            words += self.csv_to_words(csv_path)
        else:
            words += self.docx_to_words(path)
            self.words_to_csv(words, csv_path)
        if os.path.exists(wrong_file):
            words += self.csv_to_words(wrong_file)
        logging.info("DictInterfaceImplement - Totally load {} words this time.".format(len(words)))
        return list(set(words))         # 去重

    def csv_to_words(self, path: str):
        words = []
        with open(path) as f:
            file = csv.reader(f)
            for row in file:
                words += [word for word in row if self._is_word(word)]
            logging.info('DictInterfaceImplement - Words have been read in memory.')
        return words

    def docx_to_words(self, path: str):
        text = self._docx_to_text(path)
        words = self._find_words(text)
        return words

    def db_to_words(self):
        pass

    def words_to_csv(self, words: list, path: str):
        if not words:
            logging.error('DictInterfaceImplement - There are no words need to save.')
            raise Exception('Empty words.')
        with open(path, 'a', newline='', encoding='utf-8') as f:
            file = csv.writer(f)
            file.writerow(words)
            logging.info('DictInterfaceImplement - Words saved in the {}'.format(path))
        return None

    def words_to_db(self, database: DataBaseImplement, table: str, words: list):
        if not words:
            logging.error('DictInterfaceImplement - words_to_db - No words need to save.')
            return None
        if database.db is None:
            logging.error('DictInterfaceImplement - words_to_db - No database.')
            return None
        for word in words:
            if self._is_word(word):
                database.database_insert_primary_key(table, word=word)
        logging.info('DictInterfaceImplement - words_to_db - Save words to database {}.'.format(database.db))

    def _docx_to_text(self, path):
        if not os.path.exists(path):
            logging.error("DictInterfaceImplement - Can not find docx file in {}".format(path))
            raise Exception("Can not find docx file in {}".format(path))
        word_content = docx2txt.process(path)
        logging.info('DictInterfaceImplement - Successfully get the content of {}'.format(path))
        return word_content

    def _find_words(self, text):
        text_without_symbol = re.compile("\w+").findall(text)
        words = []
        for word in text_without_symbol:
            if len(word) > 3 and self._is_word(word):
                words.append(str.lower(word))
            else:
                pass
        logging.info('DictInterfaceImplement - {} words has been checked out.'.format(len(words)))
        return words

    def _is_word(self, word):
        return self.enchant.check(word)
