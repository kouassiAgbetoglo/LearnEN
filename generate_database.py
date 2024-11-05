import json
import sqlite3
import os

file_name = "Data/20k.json"
json_file = open(file_name)
data = json.load(json_file)


database = '20kWords.db'

if not os.path.isfile(database):

    connexion = sqlite3.connect(database)
    cursor = connexion.cursor()
    cursor.execute("DROP TABLE IF EXISTS WORDS")


    table ="""CREATE TABLE WORDS(word_id INTEGER PRIMARY KEY, en_translation VARCHAR(255), fr_translation VARCHAR(255));"""


    cursor.execute(table)

    for index, (_, item) in enumerate(data.items()):
        en_str = item['english']
        fr_str = item['french']
        insert_query = "INSERT INTO WORDS VALUES (?, ?, ?)"
        cursor.execute(insert_query, (index, en_str, fr_str))
    
    connexion.commit() 
    connexion.close()
    
connexion = sqlite3.connect(database)
cursor = connexion.cursor()
alter_query = "ALTER TABLE WORDS ADD COLUMN Occurrence INTEGER DEFAULT 0"
cursor.execute(alter_query)
connexion.commit() 
connexion.close()
