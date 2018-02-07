import sqlite3

class DatabaseManager(object):
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.conn.commit()
        self.cur = self.conn.cursor()

    def query(self, *arg):
        self.cur.execute(*arg)
        return self.cur

    def query_commit(self, *arg):
        self.cur.execute(*arg)
        self.conn.commit()
        return self.cur

    def commit(self):
        self.conn.commit()
        return self.cur

    def __del__(self):
        self.conn.close()