import sqlite3
import random

class ConnectDB:
    
    def __init__(self, db):
        self.database = db
    
    def connect_to_db(self, table_name):
        self.connexion = sqlite3.connect(self.database)
        cursor = self.connexion.cursor()
        cursor.execute(f'SELECT * FROM {table_name};')
        data = cursor.fetchall()
        return data
    
    def end_connection(self):
        self.connexion.close()
    
class RandomWord:
    
    def __init__(self, database, table):
        self.database = database
        self.table = table
        self.new_table = 'daily_words'
    
    def create_db(self):
        connexion = sqlite3.connect(self.database)
        cursor = connexion.cursor()
        # delete daly table 
        cursor.execute(f'DROP TABLE IF EXISTS {self.new_table}')
        create_new_table_query = f'CREATE TABLE {self.new_table}(id INTEGER PRIMARY KEY, en_translation VARCHAR(255), fr_translation VARCHAR(255))'
        cursor.execute(create_new_table_query)
        connexion.commit() 
        connexion.close()
        
    def random_database(self, sample_number=5):        
        connexion = sqlite3.connect(self.database)
        cursor = connexion.cursor()
        
        cursor.execute(f'DROP TABLE IF EXISTS {self.new_table}')
        create_new_table_query = f'CREATE TABLE {self.new_table}(id INTEGER PRIMARY KEY, en_translation VARCHAR(255), fr_translation VARCHAR(255))'
        cursor.execute(create_new_table_query)
        n = cursor.execute(f'select count(*) from {self.table}').fetchall()
        data_size = n[0][0]
        random_id = random.sample(range(1, data_size), sample_number)
        
        # get data corresponding to the IDs
        for idx, id in enumerate(random_id):
            random_data_query = f'SELECT * FROM {self.table} WHERE id == {id}'
            cursor.execute(random_data_query)
            data = cursor.fetchall()[0]
            insert_query = f'INSERT INTO {self.new_table} VALUES (?, ?, ?)'
            cursor.execute(insert_query, (idx, data[1], data[2]))
        connexion.commit() 
        connexion.close()

    
    
        
        


