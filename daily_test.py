from utils import RandomWord, ConnectDB


database = 'instance/db.sqlite3'
datatable = 'WORDS'
dailytable = 'daily_words'


db_1 = ConnectDB(database)
data1 = db_1.connect_to_db(datatable)    
daily_word = RandomWord(database, datatable)
daily_word.random_database()
daily_data = db_1.connect_to_db(dailytable)  
data_list = daily_data.copy()


