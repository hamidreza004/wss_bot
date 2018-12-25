# coding: utf-8
from settings.settings import TOKEN
from Locations.get_locations import get_location
from pprint import pprint
from state import Situation
from farsi_texts import *
from keyboards import *
import telepot
import sys
import time
from os import path
import sqlite3
from telepot.loop import MessageLoop
import datetime

from telepot.delegate import pave_event_space, per_chat_id, create_open


# from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
# from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent


def get_chat_id(msg):
    return telepot.glance(msg)[2]


class StateHandler(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(StateHandler, self).__init__(*args, **kwargs)
        self.situation = 1
        self._welcome_printed = False
        #self.connection = sqlite3.connect(os.getcwd() + '\database.db', check_same_thread=False)
        self.connection = sqlite3.connect(path.join(path.dirname(path.abspath(__file__)), "database.db"), check_same_thread=False)
        self.query = self.connection.cursor()
        self.question = ""
        self.current_lecture = ""
        self.presentation_rate = int(0)
        self.context_rate = int(0)
        self.firstMessage = True

    def move_to_next_state(self, next_move):
        self.situation = self.situation * 10 + next_move

    def reset(self):
        self.situation = 1

    def get_situation(self,msg):
        return self.situation

    def get_questions(self,msg):
        self.sender.sendMessage(text=contact_us_text, reply_markup=contact_us_keyboard1)
        if self.situation == 1:
            self.move_to_next_state(4)

    def send_question(self,msg):
        # print(query_text + '\'' + self.question + "\',\'" + msg["from"]["username"] + "\')")
        question_text = (query_text + "'" + self.question + "','" + msg["from"]["first_name"] + "'," +
                         str(msg["from"]["id"]) + ",'False')")
        self.query.execute(question_text)
        self.connection.commit()
        self.situation = 1
        self.sender.sendMessage(text=delivery_text, reply_markup=default_keyboard)
        self.firstMessage = True

    def mailbox_handler(self, msg):
        count = self.query.execute(select_count_query + str(msg["from"]["id"]) + check_read_query).fetchall()[0][0]
        self.connection.commit()
        answer = self.query.execute(select_answer_query + str(msg["from"]["id"]) + check_read_query).fetchall()
        self.connection.commit()
        if count == 0:
            self.sender.sendMessage(text="پاسخ جدیدی برای شما موجود نیست!")
        else:
            for i in answer:
                self.sender.sendMessage(text=i[0], reply_markup=read_keyboard)


    def read_handler(self, msg):
        self.query.execute(update_query + str(msg["from"]["id"]))
        self.sender.sendMessage(text="منوی اصلی!", reply_markup=default_keyboard)

    def sponsor_handler(self, msg):
        self.sender.sendMessage(text=sponsor_text, reply_markup=sponsor_keyboard)
        if self.situation == 1:
            self.move_to_next_state(6)


    def get_sponsor(self, msg):
        sahab = "سحاب"
        pushe = "پوشه"
        link = ""
        if sahab in msg["text"]:
            link = "https://sahab.ir/"
            # self.move_to_next_state(1)
        elif pushe in msg["text"]:
            link = pushe_text
            # self.move_to_next_state(2)
        if link:
            self.sender.sendMessage(text=link, reply_markup=sponsor_keyboard)

    def timeline_handler(self, msg):
        path1 = os.getcwd() + '/WSS-Day1.JPG'
        path2 = os.getcwd() + '/WSS-Day2.JPG'
        self.sender.sendPhoto(photo=open(path1,'rb'), caption="برنامه روز اول")
        self.sender.sendPhoto(photo=open(path2,'rb'), caption="برنامه روز دوم")
        # self.move_to_next_state(2)

    def speech_handler(self, msg):
        self.sender.sendMessage(text="روز را مشخص نمایید.", reply_markup=days_keyboard)
        if self.situation == 1:
            self.move_to_next_state(1)

    def day1_handler(self, msg):
        self.sender.sendMessage(text="زمان برنامه را مشخص کنید.", reply_markup=day1_keyboard)
        if self.situation == 11:
            self.move_to_next_state(1)

    def day2_handler(self, msg):
        self.sender.sendMessage(text="زمان برنامه را مشخص کنید.", reply_markup=day2_keyboard)
        if self.situation == 11:
            self.move_to_next_state(2)

    def morning_handler(self, msg):
        print(self.situation)
        if (self.situation == 111):
            self.sender.sendMessage(text="ارایه مورد نظر را مشخص کنید.", reply_markup=day1_morning_keyboard)
        else:
            self.sender.sendMessage(text="ارایه مورد نظر را مشخص کنید.", reply_markup=day2_morning_keyboard)
        if self.situation == 111 or self.situation == 112:
            self.move_to_next_state(1)

    def day1_morning_speech_handler(self, msg):
        if msg["text"] == day1_morning_buttons_texts[0]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTidSlG.jpg",
                caption="""Seyed Valiallah Fatemi-Ardakani
PhD, TOSAN""")
            self.sender.sendMessage(text="""Readiness of Iran for Digital Economy
Human Substitution with Intelligent Machines
Replacing organizations with smart platforms and principles
Asset Tokenization and Identity of All Assets (IOT) and Trading of all assets...
http://wss.ce.sharif.edu/seminar/174/""", reply_markup=day1_morning_keyboard)

        if msg["text"] == day1_morning_buttons_texts[1]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTidzdS.jpg",
                caption="""Parisa Khanipour Roshan
PhD, Georgia Institute of Technology""")
            self.sender.sendMessage(text="""Recovering high-resolution images from limited sensory data typically leads to a serious ill-posed inverse problem, demanding inversion algorithms that effectively capture the prior information. Learning a good inverse mapping from training data faces severe challenges...
http://wss.ce.sharif.edu/seminar/167/""", reply_markup=day1_morning_keyboard)

        if msg["text"] == day1_morning_buttons_texts[2]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTie2pL.jpg",
                caption="""Morteza Mardani
PhD candidate, Stanford University""")
            self.sender.sendMessage(text="""Recovering high-resolution images from limited sensory data typically leads to a serious ill-posed inverse problem, demanding inversion algorithms that effectively capture the prior information. Learning a good inverse mapping from training data faces severe challenges...
http://wss.ce.sharif.edu/seminar/149/""", reply_markup=day1_morning_keyboard)

        if msg["text"] == day1_morning_buttons_texts[3]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTie7gz.jpg",
                caption="""Shahram Ghandeharizadeh
Associate Professor, University of Southern California (USC)""")
            self.sender.sendMessage(text="""Nova proposes a departure from today's complex database managements systems (DBMSs). It uses simple components that communicate using high speed networks (RDMA) to realize a DBMS. A component may be a file system, a buffer pool manager, abstraction of data items as records, documents, and key-value pairs,...
http://wss.ce.sharif.edu/seminar/143/""", reply_markup=day1_morning_keyboard)

        if msg["text"] == day1_morning_buttons_texts[4]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTiecoG.jpg",
                caption="""Mahdi Safarnejad
PhD, Sharif University of Technology""")
            self.sender.sendMessage(text="""String similarity measures are among the most fundamental problems in computer science. The notable examples are edit distance and longest common subsequence. Known extension of these problems like tree edit distance and Ulam distance are also studied extensively...
http://wss.ce.sharif.edu/seminar/156/""", reply_markup=day1_morning_keyboard)

        if msg["text"] == day1_morning_buttons_texts[5]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTiegUX.jpg",
                caption="""Amir Rahmati
Assistant professor, Stony Brook University""")
            self.sender.sendMessage(text="""Incorporating security at the inception of a technology is a goal we frequently strive for, but rarely achieve. Most of the research in the security domain is reactive: We design attacks, defenses, and systems to expose and fix vulnerabilities...
http://wss.ce.sharif.edu/seminar/165/""", reply_markup=day1_morning_keyboard)

        if msg["text"] == day1_morning_buttons_texts[6]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTielWI.jpg",
                caption="""Ali Eslami
Staff Research Scientist, Google DeepMind""")
            self.sender.sendMessage(text=""" Scene representation—the process of converting visual sensory data into concise descriptions—is a requirement for intelligent behavior. Recent work has shown that neural networks excel at this task when provided with large, labeled datasets...
http://wss.ce.sharif.edu/seminar/148/""", reply_markup=day1_morning_keyboard)



            # self.sender.sendMessage(text="ارایه مورد نظر را مشخص کنید.", reply_markup=day1_morning_keyboard)

    def day1_afternoon_speech_handler(self, msg):
        # self.sender.sendMessage(text="ارایه مورد نظر را مشخص کنید.", reply_markup=day1_afternoon_keyboard)
        if msg["text"] == day1_afternoon_buttons_texts[0]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTi64cN.jpg",
                caption="""Aida Mousavifar
PhD candidate, EPFL""")
            self.sender.sendMessage(text="""Many tasks in machine learning and data mining, such as data diversication, non-parametric
learning, kernel machines, clustering etc., require extracting a small but representative summary
from a massive dataset. Often, such problems can be posed as maximizing a submodular set function subject to a cardinality constraint. ...
http://wss.ce.sharif.edu/seminar/141/""", reply_markup=day1_afternoon_keyboard)

        if msg["text"] == day1_afternoon_buttons_texts[1]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTi6cCb.jpg",
                caption="""Hossein Adeli
Research Scientist, Stony Brook University""")
            self.sender.sendMessage(text="""Visual attention enables prioritization, selection and further processing of visual inputs for the purpose of achieving behavioral goals, but how is this attention control learned? How does it mechanistically serve the selection of correct actions? ...
http://wss.ce.sharif.edu/seminar/139/""", reply_markup=day1_afternoon_keyboard)

        if msg["text"] == day1_afternoon_buttons_texts[2]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTi6iIN.jpg",
                caption="""Zahra Nazari
PhD, Spotify""")
            self.sender.sendMessage(text="""recommender systems have found their way into our everyday life and have spun an active research area in computer science. An important and non-trivial research problem in this area, sometimes more challenging than the design of recommender systems, is evaluating them. ...
http://wss.ce.sharif.edu/seminar/160/""", reply_markup=day1_afternoon_keyboard)

        if msg["text"] == day1_afternoon_buttons_texts[3]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTi6oPr.jpg",
                caption="""Shayan Oveis Gharan
Assistant professor, University of Washington""")
            self.sender.sendMessage(text="""A matroid is an abstract combinatorial object which generalizes the notions of spanning trees, and linearly independent sets of vectors. I will talk about an efficient algorithm based on the Markov Chain Monte Carlo technique to approximately count the number of bases of a matroid. ...
http://wss.ce.sharif.edu/seminar/152/""", reply_markup=day1_afternoon_keyboard)

        if msg["text"] == day1_afternoon_buttons_texts[4]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTi6v0S.jpg",
                caption="""Mohsen Imani
PhD candidate, UC San Diego""")
            self.sender.sendMessage(text="""We live in a world where technological advances are continually creating more data. By the year 2020, about 1.7 megabytes of new information will be created every second for each human on the planet. With the emergence of the Internet of Things, devices will generate massive data streams demanding services that pose huge technical challenges due to limited device resources. ... 
http://wss.ce.sharif.edu/seminar/166/""", reply_markup=day1_afternoon_keyboard)

        if msg["text"] == day1_afternoon_buttons_texts[5]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTi6ApB.jpg",
                caption="""Ali Zarezade
PhD, Bato Inteligente Personal Assistant""")
            self.sender.sendMessage(text="""User engagement in online social networking depends critically on the level of social activity in the corresponding platform—the number of online actions, such as posts, shares or replies, taken by their users. ...
http://wss.ce.sharif.edu/seminar/169/""", reply_markup=day1_afternoon_keyboard)


    # todo num 0 is empty
    def day2_morning_speech_handler(self, msg):
        if msg["text"] == day2_morning_buttons_texts[0]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTi9F7D.jpg",
                caption="""Amir Hosein Ghadimi
PhD, École Polytechnique Fédérale de Lausanne""")
            self.sender.sendMessage(text="""In the past few years, we have witnessed a major interest by many individuals and companies such as google, IBM and Intel among others to harness the immense capacities of the "quantum world"; and use them to our advantage for computation purposes. ...
http://wss.ce.sharif.edu/seminar/161/""", reply_markup=day2_morning_keyboard)

        if msg["text"] == day2_morning_buttons_texts[1]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTi9PM9.jpg",
                caption="""Hamid Bagheri
Assistant Professor, Nebraska-Lincoln""")
            self.sender.sendMessage(text="""The inherent complexity of large-scale software systems has always posed a significant challenge to software practitioners. On top of this, the ever increasing expansion of software into nearly every aspect of modern life is making its dependability more critical than ever. ...
http://wss.ce.sharif.edu/seminar/138/""", reply_markup=day2_morning_keyboard)

        if msg["text"] == day2_morning_buttons_texts[2]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTi9V4Q.jpg",
                caption="""Mohammad Gharib
Postdoctoral Research Fellow, IPM""")
            self.sender.sendMessage(text="""yber physical systems are simply defined as connected embedded systems,
for more smart living. A simple example is the self driving cars. In such systems,
the feedback from physical environment is required. ...
http://wss.ce.sharif.edu/seminar/154/""", reply_markup=day2_morning_keyboard)

        if msg["text"] == day2_morning_buttons_texts[3]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTiaczt.jpg",
                caption="""Mostafa Dehghani
Research Scientist, Google Brain""")
            self.sender.sendMessage(text="""A key signature of human intelligence is the ability to make "infinite use of finite means", thus having no limitation on the computational budget appears to be an essential ingredient for intelligent systems to eventually get to the human-like intelligence. ... 
http://wss.ce.sharif.edu/seminar/145/""", reply_markup=day2_morning_keyboard)

        if msg["text"] == day2_morning_buttons_texts[4]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTialYb.jpg",
                caption="""Elmira Nezamfar
Researcher at DSN lab, Sharif university of Technology""")
            self.sender.sendMessage(text="""Machine learning algorithms are achieving state-of-the-art performance in many various applications such as image processing, machine vision, speech recognition, diagnosis diseases, robotics, military, and aerospace. For decades, the usage of machine learning algorithms especially Neural Network Algorithms (NNA) has been restricted due to their complexity and high computation time of available inefficient hardware. ...
http://wss.ce.sharif.edu/seminar/173/""", reply_markup=day2_morning_keyboard)

        if msg["text"] == day2_morning_buttons_texts[5]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTiaz98g.jpg",
                caption="""Mohammad Amin Fazli
Assistant Professor, Sharif University of Technology""")
            self.sender.sendMessage(text="""Lightning Network is a novel off chain solution to Bitcoin's scalability problem. It features a peer to peer network of payment channels which can transfer value off chain. ...
http://wss.ce.sharif.edu/seminar/151/""", reply_markup=day2_morning_keyboard)

        if msg["text"] == day2_morning_buttons_texts[6]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTiaJps.jpg",
                caption="""Mohammadreza Babaei
PhD candidate, Max Planck Institute""")
            self.sender.sendMessage(text="""A growing number of people rely on social media platforms, such as Twitter and
Facebook, for their news and information needs, where users themselves play
a role in selecting the sources from which they consume information, overthrowing
traditional journalistic gatekeeping. ...
http://wss.ce.sharif.edu/seminar/142/""", reply_markup=day2_morning_keyboard)

        if msg["text"] == day2_morning_buttons_texts[7]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTiaPeW.jpg",
                caption="""Arash Einolghozati
PhD, Georgia Institute of Technology""")
            self.sender.sendMessage(text="""Machine learning algorithms such as Neural Networks are prone to adversarial attacks in which a carefully chosen example can fool the classifier. Such examples, imperceptible to human eye (in computer vision) or semantically the same (in NLP), can bring the accuracy of sophisticated networks to virtually zero. ...  
http://wss.ce.sharif.edu/seminar/168/""", reply_markup=day2_morning_keyboard)

        if msg["text"] == day2_morning_buttons_texts[8]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTiaUVr.jpg",
                caption="""Elham Havaei
PhD candidate, University of California, Irvine""")
            self.sender.sendMessage(text="""he k-leaf power graph G of a tree T is a graph whose vertices are the leaves of T and whose edges connect pairs of leaves at unweighted distance at most k in T. Recognition of the k-leaf power graphs for k < 7 is still an open problem. In this talk, we provide an algorithm for this problem for sparse leaf power graphs. ...
http://wss.ce.sharif.edu/seminar/137/""", reply_markup=day2_morning_keyboard)

            # todo nothing

    def afternoon_handler(self, msg):
        if (self.situation == 111):
            self.sender.sendMessage(text="ارایه مورد نظر را مشخص کنید.", reply_markup=day1_afternoon_keyboard)
        else:
            self.sender.sendMessage(text="ارایه مورد نظر را مشخص کنید.", reply_markup=day2_afternoon_keyboard)
        if self.situation == 111 or self.situation == 112:
            self.move_to_next_state(2)

    # todo nothing
    def day2_afternoon_speech_handler(self, msg):
        if msg["text"] == day2_afternoon_buttons_texts[0]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTibZID.jpg",
                caption="""Mohammad Hosein Rohban
Assistant professor, Sharif University of Technology""")
            self.sender.sendMessage(text="""mage-based profiling has proven to be a powerful, efficient single-cell technology for characterizing the function of small molecules and genes at large scale. In image-based – or morphological – profiling, each cell population perturbed by a genetic or small molecule reagent is measured for a pattern – or signature – of the perturbants' effect on cell state. ...
http://wss.ce.sharif.edu/seminar/153/""", reply_markup=day2_afternoon_keyboard)

        if msg["text"] == day2_afternoon_buttons_texts[1]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTic6vA.jpg",
                caption="""Meysam Alizadeh
Postdoctoral Research Associat, Princeton University""")
            self.sender.sendMessage(text="""Foreign influence efforts on democratic elections are undermining confidence in governments around the world and may have shaped outcomes from Britain to France to the United States. Since 2014 at least 65 distinct influence campaigns have targeted 18 different democracies. ... 
http://wss.ce.sharif.edu/seminar/170/""", reply_markup=day2_afternoon_keyboard)

        if msg["text"] == day2_afternoon_buttons_texts[2]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTicaJC.jpg",
                caption="""Majid Abdollah Khani
master, TOSAN""")
            self.sender.sendMessage(text="""Digital banking against traditional banking
Digital Bank Brands & Channels
Design a digital bank
Digital interactions , product and process
Digital Organizations ....
http://wss.ce.sharif.edu/seminar/171/""", reply_markup=day2_afternoon_keyboard)

        if msg["text"] == day2_afternoon_buttons_texts[3]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTicelW.jpg",
                caption="""Majid Sabbagh
Ph.D Candidate, Northeastern University""")
            self.sender.sendMessage(text="""Edge computing enables advanced on-device processing and decision making. This paradigm lowers dependence on the cloud and hence reduces the latency for critical applications and potentially enhances the privacy of users. ...
http://wss.ce.sharif.edu/seminar/140/""", reply_markup=day2_afternoon_keyboard)

        if msg["text"] == day2_afternoon_buttons_texts[4]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTicid7.jpg",
                caption="""Mohammad Mahdian
Staff Research Scientist, Google Research""")
            self.sender.sendMessage(text="""In this talk, I will given an overview of two growing field of research: mechanism design for auctions, and differential privacy. I will explain the notion of differential privacy and present some of the key results in the differential privacy literature. ...
http://wss.ce.sharif.edu/seminar/147/""", reply_markup=day2_afternoon_keyboard)

        if msg["text"] == day2_afternoon_buttons_texts[5]:
            self.sender.sendPhoto(
                photo="https://pasteboard.co/HTicmdB.jpg",
                caption="""Majid Farhadi
PhD candidate, Georgia Institute of Technology""")
            self.sender.sendMessage(text=""""Cheeger (isoperimetric) constant of a (compact Riemannian) maniforld is a positive real number defined in terms of the minimal area of a hypersurface that divides the manifold into two disjoint pieces, encapsulating a measure of bottleneckedness. ...
http://wss.ce.sharif.edu/seminar/172/""", reply_markup=day2_afternoon_keyboard)


    def location_handler(self, msg):
        self.sender.sendPhoto(photo=open(os.getcwd() + "/university_map.jpg", 'rb'),caption=location_text, reply_markup=location_keyboard)
        if self.situation == 1:
            self.move_to_next_state(3)

    def location_handler_2(self, msg):
        location = get_location(msg["text"])
        if location is not None:
            latitude, longitude = location
            self.sender.sendLocation(latitude=latitude, longitude=longitude)

    def poll_handler(self, msg):
        self.sender.sendMessage(text=poll_form_text, reply_markup=poll_keyboard)
        if self.situation == 1:
            self.move_to_next_state(6)

    def day1_morning_poll_handler(self , msg):
        self.sender.sendMessage(text="ارائه های صبح روز اول", reply_markup=day1_morning_poll_keyboard)
        if self.situation == 16:
            self.move_to_next_state(1)

    def day1_afternoon_poll_handler(self , msg):
        self.sender.sendMessage(text="ارائه های عصر روز اول", reply_markup=day1_afternoon_poll_keyboard)
        if self.situation == 16:
            self.move_to_next_state(2)

    def day2_morning_poll_handler(self, msg):
        self.sender.sendMessage(text="ارائه های صبح روز دوم", reply_markup=day2_morning_poll_keyboard)
        if self.situation == 16:
            self.move_to_next_state(3)

    def day2_afternoon_poll_handler(self, msg):
        self.sender.sendMessage(text="ارائه های عصر روز دوم", reply_markup=day2_afternoon_poll_keyboard)
        if self.situation == 16:
            self.move_to_next_state(4)

    def poll_question_handler(self, msg):
        if msg["text"] == day1_morning_poll_buttons_texts[0]:
            self.current_lecture = day1_morning_poll_buttons_texts[0],
        elif msg["text"] == day1_morning_poll_buttons_texts[1]:
            self.current_lecture = day1_morning_poll_buttons_texts[1],
        elif msg["text"] == day1_morning_poll_buttons_texts[2]:
            self.current_lecture = day1_morning_poll_buttons_texts[2],
        elif msg["text"] == day1_morning_poll_buttons_texts[3]:
            self.current_lecture = day1_morning_poll_buttons_texts[3],
        elif msg["text"] == day1_morning_poll_buttons_texts[4]:
            self.current_lecture = day1_morning_poll_buttons_texts[4],
        elif msg["text"] == day1_morning_poll_buttons_texts[5]:
            self.current_lecture = day1_morning_poll_buttons_texts[5],
        elif msg["text"] == day1_morning_poll_buttons_texts[6]:
            self.current_lecture = day1_morning_poll_buttons_texts[6],
        elif msg["text"] == day1_afternoon_poll_buttons_texts[0]:
            self.current_lecture = day1_afternoon_poll_buttons_texts[0],
        elif msg["text"] == day1_afternoon_poll_buttons_texts[1]:
            self.current_lecture = day1_afternoon_poll_buttons_texts[1],
        elif msg["text"] == day1_afternoon_poll_buttons_texts[2]:
            self.current_lecture = day1_afternoon_poll_buttons_texts[2],
        elif msg["text"] == day1_afternoon_poll_buttons_texts[3]:
            self.current_lecture = day1_afternoon_poll_buttons_texts[3],
        elif msg["text"] == day1_afternoon_poll_buttons_texts[4]:
            self.current_lecture = day1_afternoon_poll_buttons_texts[4],
        elif msg["text"] == day1_afternoon_poll_buttons_texts[5]:
            self.current_lecture = day1_afternoon_poll_buttons_texts[5],
        elif msg["text"] == day1_afternoon_poll_buttons_texts[6]:
            self.current_lecture = day1_afternoon_poll_buttons_texts[6],
        elif msg["text"] == day2_morning_poll_buttons_texts[0]:
            self.current_lecture = day2_morning_poll_buttons_texts[0],
        elif msg["text"] == day2_morning_poll_buttons_texts[1]:
            self.current_lecture = day2_morning_poll_buttons_texts[1],
        elif msg["text"] == day2_morning_poll_buttons_texts[2]:
            self.current_lecture = day2_morning_poll_buttons_texts[2],
        elif msg["text"] == day2_morning_poll_buttons_texts[3]:
            self.current_lecture = day2_morning_poll_buttons_texts[3],
        elif msg["text"] == day2_morning_poll_buttons_texts[4]:
            self.current_lecture = day2_morning_poll_buttons_texts[4],
        elif msg["text"] == day2_morning_poll_buttons_texts[5]:
            self.current_lecture = day2_morning_poll_buttons_texts[5],
        elif msg["text"] == day2_morning_poll_buttons_texts[6]:
            self.current_lecture = day2_morning_poll_buttons_texts[6],
        elif msg["text"] == day2_afternoon_poll_buttons_texts[0]:
            self.current_lecture = day2_afternoon_poll_buttons_texts[0],
        elif msg["text"] == day2_afternoon_poll_buttons_texts[1]:
            self.current_lecture = day2_afternoon_poll_buttons_texts[1],
        elif msg["text"] == day2_afternoon_poll_buttons_texts[2]:
            self.current_lecture = day2_afternoon_poll_buttons_texts[2],
        elif msg["text"] == day2_afternoon_poll_buttons_texts[3]:
            self.current_lecture = day2_afternoon_poll_buttons_texts[3],
        elif msg["text"] == day2_afternoon_poll_buttons_texts[4]:
            self.current_lecture = day2_afternoon_poll_buttons_texts[4],
        elif msg["text"] == day2_afternoon_poll_buttons_texts[5]:
            self.current_lecture = day2_afternoon_poll_buttons_texts[5],
        elif msg["text"] == day2_afternoon_poll_buttons_texts[6]:
            self.current_lecture = day2_afternoon_poll_buttons_texts[6],
        self.sender.sendMessage(text="در صورت حضور در این ارائه لطفا به کیفیت ارائه آن در قالب یک عدد از 0 تا 20 امتیاز دهید. حتما بعد از ارسال عدد موردنظر گزینه پرسش بعد را فشار دهید!", reply_markup=rate_keyboard)


    def rate_handler(self, msg):
        # if int(msg["text"]) > 20 or int(msg["text"]) < 0:
        #     self.sender.sendMessage(text="لطفا در محدوده 0 تا 20 امتیاز دهید! حتما بعد از وارد کردن عدد موردنظر ارسال را فشار دهید!", reply_markup=rate_keyboard)
        self.sender.sendMessage(text="در صورت حضور در این ارائه لطفا به کیفیت محتوای علمی آن در قالب یک عدد از 0 تا 20 امتیاز دهید. حتما بعد از ارسال عدد موردنظر گزینه ارسال امتیاز را فشار دهید!", reply_markup=rate_keyboard1)
        if self.situation // 10 == 16:
            self.move_to_next_state(1)


    def rate_handler1(self, msg):
        self.sender.sendMessage(
            text="باتشکر از نظر شما!!",
            reply_markup=default_keyboard)
        self.query.execute(rate_query + "'" + self.current_lecture[0] + "', " + str(msg["from"]["id"]) + ", '" + str(
            msg["from"]["first_name"]) + "', " + str(self.presentation_rate) + ", " + str(self.context_rate) + ")")
        self.connection.commit()
        self.situation = 1

    def previous(self, msg):
        print(self.situation)
        parent_state = self.get_situation(msg) // 10
        if parent_state == 1:
            self.sender.sendMessage(text="منوی اصلی!", reply_markup=default_keyboard)
            self.situation = parent_state
        elif parent_state == 11:
            self.sender.sendMessage(text="روز ها", reply_markup=days_keyboard)
            self.situation = parent_state
        elif parent_state == 111:
            self.situation = parent_state
            self.sender.sendMessage(text="روز اول!", reply_markup=day1_keyboard)
        elif parent_state == 112:
            self.situation = parent_state
            self.sender.sendMessage(text="روز دوم!", reply_markup=day2_keyboard)
        elif parent_state == 16:
            if datetime.datetime(2017, 12, 27, 13, 59, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 27,
                                                                                                         9, 00, 00):
                self.sender.sendMessage(text="ارائه های صبح روز اول", reply_markup=poll_first_morning_keyborad)
                self.situation = 16
            elif datetime.datetime(2017, 12, 27, 20, 00, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 27,
                                                                                                           14, 00, 00):
                self.situation = 16
                self.sender.sendMessage(text="ارائه های عصر روز اول", reply_markup=poll_first_afternoon_keyborad)
            elif datetime.datetime(2017, 12, 28, 13, 59, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 28,
                                                                                                           9, 00, 00):
                self.sender.sendMessage(text="ارائه های صبح روز دوم", reply_markup=poll_second_morning_keyboard)
                self.situation = 16
            elif datetime.datetime(2017, 12, 28, 20, 00, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 28, 14, 00, 00):
                self.sender.sendMessage(text="ارائه های عصر روز دوم", reply_markup=day1_morning_poll_keyboard)
                self.situation = 16
            else:
                self.sender.sendMessage(text="نظرسنجی تمام شد!",
                                        reply_markup=default_keyboard)
                self.situation = 1
        elif parent_state == 161:
            if datetime.datetime(2017, 12, 27, 13, 59, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 27,
                                                                                                         9, 00, 00):
                self.sender.sendMessage(text="ارائه های صبح روز اول", reply_markup=day1_morning_poll_keyboard)
                self.situation = 161
            elif datetime.datetime(2017, 12, 27, 20, 00, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 27,
                                                                                                           14, 00, 00):
                self.situation = 161
                self.sender.sendMessage(text="ارائه های عصر روز اول", reply_markup=day1_afternoon_poll_keyboard)
            elif datetime.datetime(2017, 12, 28, 13, 59, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 28,
                                                                                                           9, 00, 00):
                self.sender.sendMessage(text="ارائه های صبح روز دوم", reply_markup=day2_morning_poll_keyboard)
                self.situation = 161
            elif datetime.datetime(2017, 12, 28, 20, 00, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 28, 14, 00, 00):
                self.sender.sendMessage(text="ارائه های عصر روز دوم", reply_markup=day2_afternoon_poll_keyboard)
                self.situation = 161
            else:
                self.sender.sendMessage(text="نظرسنجی تمام شد!",
                                        reply_markup=default_keyboard)
        elif parent_state == 162:
            if datetime.datetime(2017, 12, 27, 13, 59, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 27,
                                                                                                         9, 00, 00):
                self.sender.sendMessage(text="ارائه های صبح روز اول", reply_markup=day1_morning_poll_keyboard)
                self.situation = 162
            elif datetime.datetime(2017, 12, 27, 20, 00, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 27,
                                                                                                           14, 00, 00):
                self.situation = 162
                self.sender.sendMessage(text="ارائه های عصر روز اول", reply_markup=day1_afternoon_poll_keyboard)
            elif datetime.datetime(2017, 12, 28, 13, 59, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 28,
                                                                                                           9, 00, 00):
                self.sender.sendMessage(text="ارائه های صبح روز دوم", reply_markup=day2_morning_poll_keyboard)
                self.situation = 162
            elif datetime.datetime(2017, 12, 28, 20, 00, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 28, 14, 00, 00):
                self.sender.sendMessage(text="ارائه های عصر روز دوم", reply_markup=day2_afternoon_poll_keyboard)
                self.situation = 162
            else:
                self.sender.sendMessage(text="نظرسنجی تمام شد!",
                                        reply_markup=default_keyboard)
        elif parent_state == 163:
            if datetime.datetime(2017, 12, 27, 13, 59, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 27,
                                                                                                         9, 00, 00):
                self.sender.sendMessage(text="ارائه های صبح روز اول", reply_markup=day1_morning_poll_keyboard)
                self.situation = 163
            elif datetime.datetime(2017, 12, 27, 20, 00, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 27,
                                                                                                           14, 00, 00):
                self.situation = 163
                self.sender.sendMessage(text="ارائه های عصر روز اول", reply_markup=day1_afternoon_poll_keyboard)
            elif datetime.datetime(2017, 12, 28, 13, 59, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 28,
                                                                                                           9, 00, 00):
                self.sender.sendMessage(text="ارائه های صبح روز دوم", reply_markup=day2_morning_poll_keyboard)
                self.situation = 163
            elif datetime.datetime(2017, 12, 28, 20, 00, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 28, 14, 00, 00):
                self.sender.sendMessage(text="ارائه های عصر روز دوم", reply_markup=day2_afternoon_poll_keyboard)
                self.situation = 163
            else:
                self.sender.sendMessage(text="نظرسنجی تمام شد!",
                                        reply_markup=default_keyboard)
        elif parent_state == 164:
            if datetime.datetime(2017, 12, 27, 13, 59, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 27,
                                                                                                         9, 00, 00):
                self.sender.sendMessage(text="ارائه های صبح روز اول", reply_markup=day1_morning_poll_keyboard)
                self.situation = 164
            elif datetime.datetime(2017, 12, 27, 20, 00, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 27,
                                                                                                           14, 00, 00):
                self.situation = 164
                self.sender.sendMessage(text="ارائه های عصر روز اول", reply_markup=day1_afternoon_poll_keyboard)
            elif datetime.datetime(2017, 12, 28, 13, 59, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 28,
                                                                                                           9, 00, 00):
                self.sender.sendMessage(text="ارائه های صبح روز دوم", reply_markup=day2_morning_poll_keyboard)
                self.situation = 164
            elif datetime.datetime(2017, 12, 28, 20, 00, 00) > datetime.datetime.now() > datetime.datetime(2017, 12, 28, 14, 00, 00):
                self.sender.sendMessage(text="ارائه های عصر روز دوم", reply_markup=day2_afternoon_poll_keyboard)
                self.situation = 1614
            else:
                self.sender.sendMessage(text="نظرسنجی تمام شد!",
                                        reply_markup=default_keyboard)
        elif self.situation // 100 == 16:
            self.sender.sendMessage(text="منوی اصلی!", reply_markup=default_keyboard)
            self.situation = 1

                # elif parent_state == 1111:

    def welcome(self):
        self.sender.sendMessage(text="منوی اصلی!", reply_markup=default_keyboard)
        self._welcome_printed = True

    ##TODO change this if you change keyboards.py!
    _dispatcher = {default_buttons_texts[0]:speech_handler,
                   default_buttons_texts[1]: timeline_handler,
                   default_buttons_texts[2]: location_handler,
                   default_buttons_texts[3]: mailbox_handler,
                   default_buttons_texts[4]: get_questions,
                   default_buttons_texts[5]: poll_handler,
                   default_buttons_texts[6]: sponsor_handler,

                   days_buttons_texts[0]: day1_handler,
                   days_buttons_texts[1]: day2_handler,

                   day1_morning_buttons_texts[0]: day1_morning_speech_handler,
                   day1_morning_buttons_texts[1]: day1_morning_speech_handler,
                   day1_morning_buttons_texts[2]: day1_morning_speech_handler,
                   day1_morning_buttons_texts[3]: day1_morning_speech_handler,
                   day1_morning_buttons_texts[4]: day1_morning_speech_handler,
                   day1_morning_buttons_texts[5]: day1_morning_speech_handler,
                   day1_morning_buttons_texts[6]: day1_morning_speech_handler,
                   day1_morning_buttons_texts[7]: previous,

                   day1_afternoon_buttons_texts[0]: day1_afternoon_speech_handler,
                   day1_afternoon_buttons_texts[1]: day1_afternoon_speech_handler,
                   day1_afternoon_buttons_texts[2]: day1_afternoon_speech_handler,
                   day1_afternoon_buttons_texts[3]: day1_afternoon_speech_handler,
                   day1_afternoon_buttons_texts[4]: day1_afternoon_speech_handler,
                   day1_afternoon_buttons_texts[5]: day1_afternoon_speech_handler,
                   day1_afternoon_buttons_texts[6]: previous,

                   day2_morning_buttons_texts[0]: day2_morning_speech_handler,
                   day2_morning_buttons_texts[1]: day2_morning_speech_handler,
                   day2_morning_buttons_texts[2]: day2_morning_speech_handler,
                   day2_morning_buttons_texts[3]: day2_morning_speech_handler,
                   day2_morning_buttons_texts[4]: day2_morning_speech_handler,
                   day2_morning_buttons_texts[5]: day2_morning_speech_handler,
                   day2_morning_buttons_texts[6]: day2_morning_speech_handler,
                   day2_morning_buttons_texts[7]: day2_morning_speech_handler,
                   day2_morning_buttons_texts[8]: day2_morning_speech_handler,
                   day2_morning_buttons_texts[9]: previous,


                   day2_afternoon_buttons_texts[0]: day2_afternoon_speech_handler,
                   day2_afternoon_buttons_texts[1]: day2_afternoon_speech_handler,
                   day2_afternoon_buttons_texts[2]: day2_afternoon_speech_handler,
                   day2_afternoon_buttons_texts[3]: day2_afternoon_speech_handler,
                   day2_afternoon_buttons_texts[4]: day2_afternoon_speech_handler,
                   day2_afternoon_buttons_texts[5]: day2_afternoon_speech_handler,
                   day2_afternoon_buttons_texts[6]: previous,

                   poll_texts[0]:day1_morning_poll_handler,
                   poll_texts[1]:day1_afternoon_poll_handler,
                   poll_texts[2]:day2_morning_poll_handler,
                   poll_texts[3]:day2_afternoon_poll_handler,
                   poll_texts[4]:previous,

                   day1_morning_poll_buttons_texts[0]:poll_question_handler,
                   day1_morning_poll_buttons_texts[1]:poll_question_handler,
                   day1_morning_poll_buttons_texts[2]:poll_question_handler,
                   day1_morning_poll_buttons_texts[3]:poll_question_handler,
                   day1_morning_poll_buttons_texts[4]:poll_question_handler,
                   day1_morning_poll_buttons_texts[5]:poll_question_handler,
                   day1_morning_poll_buttons_texts[6]:poll_question_handler,

                   day1_afternoon_poll_buttons_texts[0]:poll_question_handler,
                   day1_afternoon_poll_buttons_texts[1]:poll_question_handler,
                   day1_afternoon_poll_buttons_texts[2]:poll_question_handler,
                   day1_afternoon_poll_buttons_texts[3]:poll_question_handler,
                   day1_afternoon_poll_buttons_texts[4]:poll_question_handler,
                   day1_afternoon_poll_buttons_texts[5]:poll_question_handler,
                   day1_afternoon_poll_buttons_texts[6]:poll_question_handler,

                   day2_morning_poll_buttons_texts[0]:poll_question_handler,
                   day2_morning_poll_buttons_texts[1]:poll_question_handler,
                   day2_morning_poll_buttons_texts[2]:poll_question_handler,
                   day2_morning_poll_buttons_texts[3]:poll_question_handler,
                   day2_morning_poll_buttons_texts[4]:poll_question_handler,
                   day2_morning_poll_buttons_texts[5]:poll_question_handler,
                   day2_morning_poll_buttons_texts[6]:poll_question_handler,

                   day2_afternoon_poll_buttons_texts[0]:poll_question_handler,
                   day2_afternoon_poll_buttons_texts[1]:poll_question_handler,
                   day2_afternoon_poll_buttons_texts[2]:poll_question_handler,
                   day2_afternoon_poll_buttons_texts[3]:poll_question_handler,
                   day2_afternoon_poll_buttons_texts[4]:poll_question_handler,
                   day2_afternoon_poll_buttons_texts[5]:poll_question_handler,
                   day2_afternoon_poll_buttons_texts[6]:poll_question_handler,

                   rate_text[0]:rate_handler,

                   rate_text1[0]:rate_handler1,


                   day1_buttons_texts[0]: morning_handler,
                   day1_buttons_texts[1]: afternoon_handler,
                   day1_buttons_texts[2]: previous,

                   day2_buttons_texts[0]: morning_handler,
                   day2_buttons_texts[1]: afternoon_handler,
                   day2_buttons_texts[2]: previous,

                   sponsor_buttons_texts[0]: get_sponsor,
                   sponsor_buttons_texts[1]: get_sponsor,
                   sponsor_buttons_texts[2]: previous,

                   locations_buttons_texts[0]: location_handler_2,
                   locations_buttons_texts[1]: location_handler_2,
                   locations_buttons_texts[2]: location_handler_2,
                   locations_buttons_texts[3]: location_handler_2,
                   locations_buttons_texts[4]: previous,

                   contact_us_buttons_text[0]: send_question,
                   contact_us_buttons_text[1]:previous,

                   read_text[0]: read_handler
                   }

    def welcomed(self):
        self.query.execute('''''')

    def on_chat_message(self, msg):
        print(type(msg["date"]))
        # pprint(msg)
        current_millis = int(round(time.time() * 1000))
        if msg['date'] - current_millis > (5 * 60 * 1000):
            return  # skip. perhaps bot was down and this is an outdated message

        # current_millis = int(round(time.time() * 1000))
        # if msg['date'] - current_millis > (5 * 60 * 1000):
        #     return
        if not self._welcome_printed:
            self.welcome()
            # self.query.execute(insert_chat_ids_query + str(msg["from"]["id"]) + ')')
            self.connection.commit()
            return
        else:
            if self.situation <= 0:
                self.situation = 0
                self.sender.sendMessage(text="منوی اصلی!", reply_markup=default_keyboard)
            if msg["text"] in StateHandler._dispatcher:
                (StateHandler._dispatcher[msg["text"]])(self, msg)
            elif self.get_situation(msg) == 14:
                if self.firstMessage:
                    self.firstMessage = False
                    self.sender.sendMessage(text="لطفا بعد از فرستادن پیام های خود گزینه ارسال را فشار دهید", reply_markup=contact_us_keyboard)
                self.question += msg["text"] + "\n"
                print(self.question)
            elif self.situation // 10 == 16:
                self.presentation_rate = int(msg["text"])
            elif self.situation // 100 == 16:
                self.context_rate = int(msg["text"])
            else:
                pass  # invalid msg

            # TODO handle: not sending responses to messages sent when bot was down ...


# bot = telepot.Bot(TOKEN)
# print(bot.getMe())

bot = telepot.DelegatorBot('797548891:AAHTRcDFwAVb1V7ru2XhszTLZKq9TF8GzJs', [
    pave_event_space()(
        per_chat_id(), create_open, StateHandler, timeout=2 * 24 * 60 * 60),  # timeout = 2 days?
])
start_time_ms = datetime.datetime

MessageLoop(bot).run_forever()

# OR THIS METHOD:

# MessageLoop(bot).run_as_thread()
# while 1:
#     time.sleep(5)
# print('Listening ...')
