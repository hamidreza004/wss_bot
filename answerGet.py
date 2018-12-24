import sqlite3
import os

connection = sqlite3.connect(os.getcwd() + '\database.db', check_same_thread=False)
query = connection.cursor()

UserMessages = open(os.getcwd() + '/Messages.txt', 'w', encoding="utf-8")
a = query.execute('''select t1, telegram_id, chat_id from contacts''').fetchall()
for i in a:
    UserMessages.write(str(i[2]) + " " + i[1] + " said: " + i[0])


# query.execute('''insert into contacts values('سلام', 'sajjad', 546498413, 'False')''')
# connection.commit()
