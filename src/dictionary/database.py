import logging
import sqlite3


class DataBase(object):
    # create the object
    def __new__(cls):
        # create a new object
        obj = super().__new__(cls)
        return obj

    # initialize the object’s attributes
    def __init__(self):
        # public var
        self.db = None

    def database_create(self, database: str='../words.db'):
        __conn = sqlite3.connect(database)
        self.db = __conn.cursor()
        logging.info('DataBase - _database_create - open database {}'.format(database))
        return __conn.cursor()

    def database_create_table(self, table: str, **kwargs):
        attrs = ','.join([str(key)+' '+str(kwargs[key]) for key in kwargs])
        command = 'create table if not exists {}({})'.format(table, attrs)
        self.db.execute(command)

    def database_del_table(self, table: str):
        command = 'drop table {}'.format(table)
        self.db.execute(command)

    def database_add_column(self, table: str, **kwargs):
        # 判断表中是否存在该列，若不存在则添加
        res = self.db.execute("select * from {}".format(table))
        names = list(map(lambda x: x[0], res.description))
        if not {*kwargs.keys()}.issubset(names):
            attrs = ','.join([str(key)+' '+str(kwargs[key]) for key in kwargs])
            command = 'alter table {} add column {}'.format(table, attrs)
            self.db.execute(command)


if __name__ == '__main__':
    words_db = DataBase()
    words_db.database_create()
    words_db.database_create_table('main', word='varchar(255) primary key', mean='text')
    words_db.database_add_column('main', wrong='int')
