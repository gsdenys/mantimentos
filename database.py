import logging
import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL')

class DBHelper:
    def __init__(self, dbname=DATABASE_URL):
        self.dbname = dbname
        self.conn = psycopg2.connect(dbname)
        

    def setup(self):
        stmt = '''CREATE TABLE IF NOT EXISTS items (
	                id SERIAL PRIMARY KEY,
                    description TEXT NOT NULL UNIQUE,
                    status INTEGER NOT NULL
                );'''
        try:     
            cur = self.conn.cursor()
            
            cur.execute(stmt)
            self.conn.commit()
            
            cur.close()
        except Exception as error:
            logging.error('Could not connect to the Database.')
            logging.error('Cause: {}'.format(error))
        

    def add_item(self, description):
        stmt = "INSERT INTO items (description, status) VALUES (%s, %s)"
        args = (description.lower().strip(), 0)
        
        cur = self.conn.cursor()
        
        cur.execute(stmt, args)
        self.conn.commit()
        
        cur.close()

    # def delete_item(self, item_text):
    #     stmt = "DELETE FROM items WHERE description = (?)"
    #     args = (item_text, )
    #     self.conn.execute(stmt, args)
    #     self.conn.commit()

    def get_items(self):
        stmt = "SELECT * FROM items"
        
        cur = self.conn.cursor()
        cur.execute(stmt)
        
        dt = [(x[0], x[1], x[2]) for x in cur.fetchall()]
        cur.close()
        
        return dt
    
    
    def get_items_by_status(self, status):
        stmt = "SELECT * FROM items WHERE status = (?)"
        args = (status,)
        
        cur = self.conn.cursor()
        cur.execute(stmt, args)
        
        dt = [(x[0], x[1], x[2]) for x in cur.fetchall()]
        cur.close()
        
        return dt
