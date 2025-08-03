import mysql.connector # type: ignore
import logging

class MySQLHandler:
    def __init__(self, config):
        self.conn = mysql.connector.connect(
            host=config['host'], user=config['user'],
            password=config['password'], database=config['database']
        )
        self.cursor = self.conn.cursor()

    def create_tables(self):
        with open("sql/create_tables.sql") as f: # type: ignore
            commands = f.read().split(";")
        for c in commands:
            if c.strip():
                self.cursor.execute(c)
        self.conn.commit()
        logging.info("Tables created/verified")

    def insert_data(self, table, data):
        if not data:
            return
        cols = data[0].keys()
        qry = f"INSERT IGNORE INTO {table} ({','.join(cols)}) VALUES ({','.join(['%s']*len(cols))})"
        self.cursor.executemany(qry, [tuple(d.values()) for d in data])
        self.conn.commit()

    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
