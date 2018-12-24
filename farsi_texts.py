# coding: utf-8
default_buttons_texts = [
    "اطلاعات سخنرانی ها"
    ,
            "برنامه زمان بندی"
    ,
            "مکان ها"
    ,
            "صندوق پیام"
    ,
            "ارتباط با ما"
    ,
            "نظرسنجی"
    ,
            "معرفی و فرصت های شغلی حامیان برنامه"
]

sponsor_buttons_texts = [
    "سحاب"
    ,
    "پوشه"
    ,
    "بازگشت"
]

locations_buttons_texts = [
        "تالارها"
    ,
        "سالن جابر"
    ,
        "مسجد"
    ,
        "غذاخوری"
    ,
        "بازگشت"
]


contact_us_buttons_text =[
    "ارسال"
    ,
    "بازگشت"
]

contact_us_buttons_text1 = [
    "بازگشت"
]

days_buttons_texts = [
    "روز اول"
    ,
    "روز دوم"
    ,
    "بازگشت"

]
day1_buttons_texts = [
    "صبح",
    "بعد از ظهر"
    ,
    "بازگشت"

]
day2_buttons_texts = [
    "صبح",
    "بعد از ظهر"
    ,
    "بازگشت"
]
day1_morning_buttons_texts = [
    "Cache Augmented Data Stores: Solutions and Opportunities",
    "Coding for Computing",
    "Towards Incremental Computation of Advanced Analytics",
    "Genomic Characterization and Applications of Modern Sequencing Technologies",
    "Population Stratification: Reliable Inference and Association Mapping",
    "Optimization and Intervention in Networks",
    "Distributed Load Balancing in Cache Network",
    "بازگشت"
]
day1_afternoon_buttons_texts = [
    "Learning Safe Policies in Sequential Decision-Making",
    "Integrating Algorithmic Methods and Artificial Intelligence: A New Paradigm in Bioinformatics",
    "Continuous Authentication Based on BioAura",
    "Decentralized collaborative work",
    "Discriminating Clinical Phases of Recovery From Major Depressive Disorder using the Dynamics of Facial Expression",
    "CloudPath: A Multi-Tier Cloud Computing Framework",
    "Solving association problems with Convex Co-embedding",
    "بازگشت"
]
day2_morning_buttons_texts = [
    "TBA",
    "On information theoretic secrecy",
    "Stability-Aware Routing and Scheduling for Control Applications in Ethernet Networks",
    "Early detection of Crossfire attacks using deep learning",
    "Monotone Measures for Non-local Correlations",
    "Large scale learning: challenges and solutions",
    "Maximizing the Spread of Social Norms in Social Networks",
    "بازگشت"
]

day2_afternoon_buttons_texts = [
    "Computational Social Science, a New Approach to Old Problems",
    "Practical, lightweight formal analysis of software systems",
    "Data Science : Lessons learned from analysis of a massive mobile phone dataset",
    "Tampering Attacks in Cryptography and Learning​",
    "Stochastic Submodular Maximization",
    "Cost-Effective Storage Architectures for Emerging Big Data Applications",
    "Fine-mapping the Favored Mutation in a Positive Selective Sweep",
    "بازگشت"
]


read_text = [
    "خواندم"
]



# TODO on change any of these texts or the order: change get_locations() & _dispatcher
# TODO be careful with persian & arabic "k" and "ye"
# TODO they are different! == may become broken!
# example: لوکیشن != لوکیشن if one of "ye"s or "ke"s was typed on arabic keyboard and the other one on farsi keyboard

welcome_text = "" + \
"""
سلام

به بات سیمنار زمستانه مباحث پیشرفته علوم کامپیوتر خوش آمدید!

لطفاً گزینه مورد نظرتان را انتخاب فرمایید.

"""

sponsor_text = "" + \
"""
لطفا حامی مورد نظر خود را انتخاب نمایید:)
"""
sahab_link = "" + \
""" https://sahab.ir/
"""
speech_text = "" + \
"""
به کدام زمینه علاقه مندید؟
"""

location_text = "" +\
    """
نقشه دانشگاه صنعتی شریف
برای دریافت لوکیشن دقیق مکان مورد نظر خود، گزینه‌ی آن را انتخاب نمایید.
    """

mail_box = "" +\
    """
    صندوق پیام
    """

contact_us_text = "" + \
    """
    هر گونه پیشنهاد و انتقاد و یا هر گونه سوالی دارید در این قسمت مطرح کنید:
    """

query_text = "" + \
    """
insert into contacts \nvalues(
    """

delivery_text = "" + \
    """
پیام شما با موفقیت ارسال شد!
پاسخ خود را در صندوق پیام دریافت کنید :)
    """

select_count_query = "" +\
    """
    select count(*) from answers
    where chat_id =
    """

select_answer_query = "" +\
    """
    select t1 from answers
    where chat_id =
    """

update_query = "" +\
    """
    update answers
    set read = 'True'
    where chat_id =
    """

check_read_query = "" +\
    """

and read = 'False'
    """


insert_chat_ids_query = "" +\
    """
    insert into chat_ids
    values(
    """


day1_morning_poll_buttons_texts=[
    "سخنرانی کلیدی: شهرام قندهاری زاده (9:30)",
    "امیر شیخها(11:00)",
    "ایمان حاجی رسولی‌ها(11:00)",
    "محمدعلی مداح علی (11:00)",
    "پویا شریعت پناهی(12:00)",
    "مهرداد فرج تبار(12:00)",
    "ابوالفضل مطهری (12:00)",
    "بازگشت"
]

day1_afternoon_poll_buttons_texts = [
    "سخنرانی کلیدی محمد قوام زاده (14:30)",
    "نیلوفر صالحی (15:30)",
    "ارسلان محسن نیا (15:30)",
    "علی شریفی زارچی (15:30)",
    "فرزانه میرزازاده (17:00)",
    "سید حسن مرتضوی (17:00)",
    "سحر هراتی (17:00)",
    "بازگشت"
]

day2_morning_poll_buttons_texts = [
    "سخنرانی کلیدی: محمد مهدیان (09:00)"
    ,
    "مصطفی رضا زاد (10:00)"
    ,
    "روح‌الله محفوظی (10:00)"
    ,
    "مهدی جعفری سیاوشانی(10:00)"
    ,
    "امین فضلی (12:00)"
    ,
    "هادی دانشمند (12:00)"
    ,
    "سلمان ابوالفتح بیگی (12:00)"
    ,
    "بازگشت"
]

day2_afternoon_poll_buttons_texts = [
    "سخنرانی کلیدی: طه یاسری (14:30)"
    ,
    "محمد محمودی (15:30)"
    ,
    "بهنام بحرک (15:30)"
    ,
    "حمید باقری (15:30)"
    ,
    "صبا احمدیان (17:00)"
    ,
    "محمدرضا کریمی (17:00)"
    ,
    "مهرداد بختیاری (17:00)"
    ,
    "بازگشت"
]

poll_texts = [
    "صبح روز اول"
    ,
    "عصر روز اول"
    ,
    "صبح روز دوم"
    ,
    "عصر روز دوم"
    ,
    "بازگشت"
]

rate_text =[
    "پرسش بعد"
    ,
    "بازگشت"
]

rate_text1 =[
    "ارسال امتیاز"
    ,
    "بازگشت"
]


rate_query = "" +\
"""
insert into ratings values(
"""


pushe_text = "" +\
    """
🔷فرصت های شغلی در سرویس پوشه🔷


🔹Fronted Developer

     • ReactJs + Redux
     • HTML 5 + CSS

----------------------------------------------
🔹Backend Developer

     • Proficient in either:
            o Django
            o NodeJs

     • Familiar with:
            o MongoDB
            o Redis
            o Celery
            o Kafka
            o Docker

----------------------------------------------
🔹Client:
     •  iOS
     • Android

----------------------------------------------
🔹Data Analyst:

     • SQL
     • SciPy Ecosystem (numpy, matplotlib, seaborn, ...)
     • Strong Background in Statistics

----------------------------------------------
🔹Data Scientist:

     • Knowledgeable in:
             o Machine Learning
             o Recommender Systems

     • Proficient in one of:
             o Tensorflow
             o Scikit Learn
             o PyTorch

     •Familiar with:
             o Hadoop Echosystem

----------------------------------------------
درصورت تمایل می توانید رزومه ی خود را به
Jobs@pushe.co
ارسال نمایید
@pushe
    """


poll_form_text = "" +\
    """
    🔸با تشکر از همه عزیزانی که در "سومین سمینار زمستانۀ مباحث پیشرفته در علوم و مهندسی کامپیوتر " همراه ما بودند، خواهشمندیم به منظور یاری‌رسانی در جهت برگزاری بهتر این سمینار در سال‌های آتی نظرات خود را از طریق فرم زیر به ما انتقال دهید:
🔹 goo.gl/rU4a2P
    """