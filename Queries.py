import sqlite3
import os

connection = sqlite3.connect(os.getcwd() + '\database.db', check_same_thread=False)
query = connection.cursor()

ratings = open(os.getcwd() + '/ratings.txt', 'w', encoding="utf-8")
a = query.execute('''select * from ratings''').fetchall()
connection.commit()
for i in a:
    ratings.write(i[0] + ' ' + str(i[1]) + " " + i[2] + " " + " " + str(i[3]) + " " + str(i[4]) + '\n')

chat_ids = open(os.getcwd() + '/chat_ids.txt', 'w', encoding="utf-8")
a = query.execute('''select distinct(chat_ids) from chat_ids''').fetchall()
for i in a:
    chat_ids.write(str(i[0]) + '\n')

# query.execute('''delete from ratings where 1 = 1''')
# connection.commit()



