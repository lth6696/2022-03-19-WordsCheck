import logging

from src.actor.ActorModel import Actor
from src.message.MsgModel import Message
from src.dictionary.DictDataBase import DataBaseImplement


class DictActorImplement(Actor):
    def __init__(self, name: str, table: str, ui_handler):
        super(DictActorImplement, self).__init__()

        self.name = name
        self.table = table
        self.database = self.__init_database()
        self.userinterfacer = ui_handler

    def run(self):
        while True:
            msg = self.recv()
            if not isinstance(msg, Message):
                continue
            logging.info('DictActorImplement - run - Message info {}'.format(msg.__dict__))
            if msg.recv != 'database':
                continue
            try:
                getattr(self, msg.func)(**msg.args)
            except:
                logging.error('DictActorImplement - run - Request method {} not exist or arguments {} wrong.'
                              .format(msg.func, msg.args))

    def update(self, word: str, **kwargs):
        try:
            self.database.database_connect(self.name)
            self.database.database_update_values(self.table, word, **kwargs)
            self.database.conn.commit()
            self.database.conn.close()
            logging.info('DictActorImplement - update - Word \'{}\' is update {}.'.format(word, kwargs))
        except:
            logging.error('DictActorImplement - update - Word \'{}\' do not update successfully.'.format(word))

    def insert(self, words: list, range: str):
        self.database.database_connect(self.name)
        for word in words:
            self.database.database_insert_row(self.table, (word, '', range))
        self.database.conn.commit()
        self.database.conn.close()
        logging.info('DictActorImplement - insert - Insert all of words.')

    def find_wrong_words(self):
        self.database.database_connect(self.name)
        records = self.database.database_find_records(self.table,
                                                      columns=['word'],
                                                      const={'level': 'wrong', 'range': '071075'})
        wrong_words = [word[0] for word in records]
        self.userinterfacer.send(Message('database', 'ui', '_add_wrong_words', {'words': wrong_words}))

    def __init_database(self):
        database = DataBaseImplement()
        database.database_connect(self.name)
        database.database_create_table(self.table,
                                       word='TEXT PRIMARY KEY',
                                       level='TEXT',
                                       range='TEXT')
        logging.info('DictActorImplement - __init_database - Initialize a database.')
        return database
