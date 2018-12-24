import sqlite3
import os
#
connection = sqlite3.connect(os.getcwd() + '\database.db', check_same_thread=False)
query = connection.cursor()

# # print(query.execute('''select * from contacts''').fetchall())
# name1 = "'#AliAkbarMoeini'"
# answer1 ="""
#     سلام
#      اسلاید ها حتما تا دوهفته دیگر همراه با فیلم های سمینار ها تا دو هفته آینده در سایت بارگیری میشوند.
#     """
# name2 = "'Niloofar'"
# answer2 ="""سلام
#  حتما سعی میشود در دوره های آینده این کار انجام شود
#  از پیشنهادتون متشکریم
# از کمبود های این دوره هم متاسفیم."""
#
#
name3 = "'Sajjad'"
answer3 = "" +\
    """
    سلام
سینا
    """
# # query.execute("insert into answers values('سلام با عرض پوزش از این بابت. خیر اطلاعات دیگری در ایمیل نبود.', 'Ehsan', 73675932, 'False')")
# # query.execute("insert into answers values('سلام نوش جان خوشحالیم که راضی بودین', 'Ali', 63961974, 'False')")
# # query.execute("insert into answers values('سلام بله در همکف دانشکده شیمی است.', "+ name + ", 428768175, 'False')")
# # print("insert into answers values('سلام بله در همکف دانشکده شیمی است.', "+ name + ", 428768175, 'False')")
# # query.execute("insert into answers values('سلام وقت بخیر دوست عزیز ما قابلیت ثبت‌نام و پذیرش برای یک ارائه رو هم داریم', "+ name + ", 67600171, 'False')")
# query.execute("insert into answers values('" + answer1 + "', " + name1 + ", 95932289, 'False')")
# connection.commit()
# query.execute("insert into answers values('" + answer2 + "', " + name2 + ", 105682537, 'False')")
# connection.commit()
query.execute("insert into answers values('" + answer3 + "', " + name3 + ", 105566991, 'False')")
connection.commit()

# # print(query.execute("").fetchall())
