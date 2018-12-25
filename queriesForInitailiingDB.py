import sqlite3
import os

connection = sqlite3.connect(os.getcwd() + '\database.db', check_same_thread=False)
query = connection.cursor()

connection = sqlite3.connect(os.getcwd() + '\database.db', check_same_thread=False)
query = connection.cursor()
query.execute('''create table answers(t1 text, id varchar(30), chat_id integer, read varchar(5))''')
connection.commit()
connection = sqlite3.connect(os.getcwd() + '\database.db', check_same_thread=False)
query = connection.cursor()
query.execute('''create table chat_ids (chat_ids int)''')
connection.commit()
connection = sqlite3.connect(os.getcwd() + '\database.db', check_same_thread=False)
query = connection.cursor()
query.execute('''create table ratings (lecturer_name varchar(100), chat_id int, telegram_id varchar(30), presentation_rate int, context_rate int)''')
connection.commit()
#query.execute('''drop table contacts''')
#connection.commit()
query.execute('''create table contacts(t1 text, telegram_id varchar(30), chat_id integer, is_answered varchar(5))''')
connection.commit()
