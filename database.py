import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL')

class DBHelper:
    def __init__(self, dbname=DATABASE_URL):
        self.dbname = dbname
        self.conn = psycopg2.connect(dbname)

    def setup(self):
        stmt = '''CREATE TABLE IF NOT EXISTS items (
	                id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL UNIQUE,
                    status INTEGER NOT NULL
                );'''
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, description):
        stmt = "INSERT INTO items (description, status) VALUES (?, ?)"
        args = (description.lower().strip(), 0)
        self.conn.execute(stmt, args)
        self.conn.commit()

    # def delete_item(self, item_text):
    #     stmt = "DELETE FROM items WHERE description = (?)"
    #     args = (item_text, )
    #     self.conn.execute(stmt, args)
    #     self.conn.commit()

    def get_items(self):
        stmt = "SELECT * FROM items"
        return [(x[0], x[1], x[2]) for x in self.conn.execute(stmt)]
    
    def get_items_by_status(self, status):
        stmt = "SELECT * FROM items WHERE status = (?)"
        args = (status,)
        
        return [(x[0], x[1], x[2]) for x in self.conn.execute(stmt, args)]

