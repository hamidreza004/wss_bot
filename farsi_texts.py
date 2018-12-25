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
    "Sponser",
    "Why not ask users?",
    "Neural Proximal Gradient Descent with GANs for Compressive Imaging",
    "Nova:  Diffused Database Processing Using Clouds of Components",
    "Fast Algorithms for Edit Distance and Other Similarity Measures",
    "Tackling the security and privacy challenges of emerging technologies across the computing stack",
    "Neural scene representation and rendering",
    "بازگشت"
]
day1_afternoon_buttons_texts = [
    "Data Summarization on Massive Data Streams",
    "Learning to attend in a brain-inspired deep neural network",
    "Did you enjoy your Discover Weekly? Challenges in the design and evaluation of recommender systems",
    "Strongly log concave polynomials, high dimensional simplicial complexes, and an FPRAS for counting Bases of Matroids",
    "Brain-Inspired Hyperdimensional Computing: An Efficient Cognitive Machine",
    "Steering Social Activity: A Stochastic Optimal Control Point Of View",
    "بازگشت"
]
day2_morning_buttons_texts = [
    "Quantum world",
    "Automating Pragmatic Software Dependability",
    "Cyber physical systems",
    "Universal Transformer: Toward the Big Dream of Universal AI",
    "Reconfigurable Architecture for Neural Networks",
    "Lightning Network: Problems and Research Opportunities",
    "Social Computing",
    "Adversarial examples and training in machine learning",
    "Parameterized Leaf Power Recognition via Embedding into Graph Products",
    "بازگشت"
]

day2_afternoon_buttons_texts = [
    "Functional annotation of human genes and alleles using image-based profiling",
    "Foreign Influence Operations on Social Media: An Overview of Academic Research",
    "Titanium-AI, the evolution of banking (Intelligent, System of Engagement and System of Insight)",
    "Challenges and opportunities in deploying machine learning systems on edge devices",
    "Auctions, Mechanism Design, and Differential Privacy",
    "On origins and applications of the KLS conjecture",
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
    "پریسا خانیپور روشن (10:30)",
    "مرتضی مردانی (10:30)",
    "شهرام قندهاری‌ زاده (10:30)",
    "مهدی صفرنژاد (11:45)",
    "امیر رحمتی (11:45)",
    "علی اسلامی (11:45)",
    "بازگشت"
]

day1_afternoon_poll_buttons_texts = [
    "آیدا موسوی‌فر (14:00)",
    "حسین عادلی (14:00)",
    "زهرا نظری (14:00)",
    "شایان اویس‌قران (15:15)",
    "محسن ایمانی (15:15)",
    "علی زارع‌زاده (15:15)",
    "بازگشت"
]

day2_morning_poll_buttons_texts = [
    "امیرحسین قدیمی (09:00)",
    "حمید باقری (09:00)",
    "محمد غریب (09:00)",
    "مصطفی دهقانی (10:15)",
    "المیرا ناظم‌فر (10:15)",
    "محمدامین فضلی (10:15)",
    "محمدرضا بابایی (11:30)",
    "آرش عین‌القضاتی (11:30)",
    "الهام هوایی (11:30)",
    "بازگشت"
]

day2_afternoon_poll_buttons_texts = [
    "محمدحسین رهبان (14:00)",
    "میثم علی‌زاده (14:00)",
    "مجید عبدالله‌خانی (14:00)",
    "مجید صباغ (15:15)",
    "محمد مهدیان (15:15)",
    "مجید فرهادی (15:15)",
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
    با تشکر از شما که در چهارمین سمینار زمستانه همراه ما هستیم، از اینکه ما را با نظرات سازنده‌تان یاری می‌کنید پیشاپیش قدردانیم.
    """