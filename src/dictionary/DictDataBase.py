import logging
import sqlite3


class DataBaseImplement(object):
    # create the object
    def __new__(cls):
        # create a new object
        obj = super().__new__(cls)
        return obj

    # initialize the object’s attributes
    def __init__(self):
        # public var
        self.conn = None
        self.db = None

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def database_connect(self, database: str):
        self.conn = sqlite3.connect(database)
        self.db = self.conn.cursor()
        logging.info('DataBaseImplement - database_connect - open database {}'.format(database))
        return self.conn

    def database_create_table(self, table: str, **kwargs):
        attrs = ','.join([str(key)+' '+str(kwargs[key]) for key in kwargs])
        command = 'create table if not exists {} ({});'.format(table, attrs)
        self.db.execute(command)
        logging.info('DataBaseImplement - database_create_table - created or connected to table {}'.format(table))

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
            logging.info('DataBase - database_add_column - Add column {} to table {}'.format(attrs, table))
        else:
            logging.error('DataBase - database_add_column - Table {} have following columns {}'.format(table, names))

    def database_insert_primary_key(self, table: str, **kwargs):
        try:
            colums = ','.join(list(kwargs.keys()))
            values = ','.join(['\''+str(kwargs[key])+'\'' for key in kwargs])
            command = 'insert or ignore into {} ({}) values ({});'.format(table, colums, values)
            self.db.execute(command)
        except:
            logging.error('DataBase - database_insert_primary_key - Can not insert key into table {}'.format(table))

    def database_insert_row(self, table: str, record: tuple):
        # command = "select name from sqlite_master where type='table'"
        # exist_tables = list(*self.db.execute(command))
        try:
            # INSERT INTO TABLE_NAME VALUES (value1,value2,value3,...valueN);
            command = 'insert into {} values {}'.format(table, record)
            self.db.execute(command)
            logging.info('DataBase - database_insert_row - Insert record {}'.format(record))
        except:
            logging.error('DataBase - database_insert_row - Can not insert record into table {}'.format(table))

    def database_insert_records(self, table: str, records: list):
        command = "select name from sqlite_master where type='table'"
        exist_tables = list(*self.db.execute(command))
        if table in exist_tables:
            for record in records:
                self.database_insert_row(table, record)
            logging.info('DataBase - database_insert_records - Insert Records.')
        else:
            logging.error('DataBase - database_insert_records - Can not insert record into table {}'.format(table))

    def database_find_records(self, table: str):
        command = "select name from sqlite_master where type='table'"
        exist_tables = list(*self.db.execute(command))
        if table in exist_tables:
            command = 'select * from {}'.format(table)
            records = self.db.execute(command)
            print(*records)

    def database_update_values(self, table: str, word: str, **kwargs):
        try:
            attrs = ','.join([str(key)+'=\''+str(kwargs[key])+'\'' for key in kwargs])
            command = "update {} set {} where word=\'{}\'".format(table,attrs, word)
            self.db.execute(command)
        except:
            logging.error('DataBase - database_update_values - Failed to update values.')
            raise Exception()


if __name__ == '__main__':
    table = 'test'
    word = ('abandon', 'give88', 0)
    words_db = DataBaseImplement()
    print(type(words_db))
    words_db.database_connect('../words.db')
    # words_db.database_del_table(table)
    # words_db.database_create_table(table,
    #                                word='TEXT PRIMARY KEY',
    #                                level='TEXT',
    #                                range='TEXT')
    words_db.database_insert_primary_key(table, word='polish')
    words_db.database_find_records(table)
    words_db.conn.commit()
