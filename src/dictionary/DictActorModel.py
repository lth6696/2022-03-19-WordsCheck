import logging

from src.actor.ActorModel import Actor
from src.message.MsgModel import Message
from src.dictionary.DictDataBase import DataBaseImplement


class DictActorImplement(Actor):
    def __init__(self, name: str, table: str):
        super(DictActorImplement, self).__init__()

        self.name = name
        self.table = table
        self.database = self.__init_database()

    def run(self):
        while True:
            msg = self.recv()
            if not isinstance(msg, Message):
                continue
            if msg.recv != 'database':
                continue
            getattr(self, msg.func)(msg.args)

    def insert(self, row):
        print(row)

    def __init_database(self):
        database = DataBaseImplement()
        database.database_connect(self.name)
        database.database_create_table(self.table,
                                       word='VARCHAR(255) PRIMARY KEY',
                                       level='VARCHAR(255)',
                                       range='VARCHAR(255)')
        logging.info('DictActorImplement - __init_database - Initialize a database.')
        return database
