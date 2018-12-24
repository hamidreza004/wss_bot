import sqlite3
import os

con = sqlite3.connect(os.getcwd() + '\database.db', check_same_thread=False)
query = con.cursor()
query.execute('''delete from answers where 1 = 1''')
con.commit()
query.execute('''delete from contacts where 1 = 1''')
con.commit()
query.execute('''delete from chat_ids where 1 = 1''')
con .commit()
query.execute('''delete from ratings where 1 = 1''')
con .commit()