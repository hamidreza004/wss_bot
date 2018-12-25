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
import os
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
        self.connection = sqlite3.connect(os.getcwd() + '\database.db', check_same_thread=False)
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
                photo="http://wss.ce.sharif.edu/media/cache/67/8e/678e6147ccfb1dbf4c18d117c1c03b4f.jpg",
                caption="""Seyed Valiallah Fatemi-Ardakani
            PhD, TOSAN""")
            self.sender.sendMessage(text="""Readiness of Iran for Digital Economy
Human Substitution with Intelligent Machines
Replacing organizations with smart platforms and principles
Asset Tokenization and Identity of All Assets (IOT) and Trading of all assets...
            http://wss.ce.sharif.edu/seminar/174/""", reply_markup=day1_morning_keyboard)

        if msg["text"] == day1_morning_buttons_texts[1]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/e9/d8/e9d8af4bc1c208d2747b2616641f7cc1.jpg",
                caption="""Parisa Khanipour Roshan
            PhD, Georgia Institute of Technology""")
            self.sender.sendMessage(text="""Recovering high-resolution images from limited sensory data typically leads to a serious ill-posed inverse problem, demanding inversion algorithms that effectively capture the prior information. Learning a good inverse mapping from training data faces severe challenges...
            http://wss.ce.sharif.edu/seminar/167/""", reply_markup=day1_morning_keyboard)

        if msg["text"] == day1_morning_buttons_texts[2]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/1f/1a/1f1a64678700d58b19b6e0fe474b793c.jpg",
                caption="""Morteza Mardani
            PhD candidate, Stanford University""")
            self.sender.sendMessage(text="""Recovering high-resolution images from limited sensory data typically leads to a serious ill-posed inverse problem, demanding inversion algorithms that effectively capture the prior information. Learning a good inverse mapping from training data faces severe challenges...
            http://wss.ce.sharif.edu/seminar/149/""", reply_markup=day1_morning_keyboard)

        if msg["text"] == day1_morning_buttons_texts[3]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/6a/af/6aaf05c67b0f85f4a8ea2458f35c99b2.jpg",
                caption="""Shahram Ghandeharizadeh
                Associate Professor, University of Southern California (USC)""")
            self.sender.sendMessage(text="""Nova proposes a departure from today's complex database managements systems (DBMSs). It uses simple components that communicate using high speed networks (RDMA) to realize a DBMS. A component may be a file system, a buffer pool manager, abstraction of data items as records, documents, and key-value pairs,...
                                http://wss.ce.sharif.edu/seminar/143/""", reply_markup=day1_morning_keyboard)

        if msg["text"] == day1_morning_buttons_texts[4]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/23/cf/23cf2a45977c6af3b71ac41297fc65f8.jpg",
                caption="""Mahdi Safarnejad
            PhD, Sharif University of Technology""")
            self.sender.sendMessage(text="""String similarity measures are among the most fundamental problems in computer science. The notable examples are edit distance and longest common subsequence. Known extension of these problems like tree edit distance and Ulam distance are also studied extensively...
            http://wss.ce.sharif.edu/seminar/156/""", reply_markup=day1_morning_keyboard)
        if msg["text"] == day1_morning_buttons_texts[5]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/dd/8c/dd8c810cc32187001ae0d1bb51a05705.jpg",
                caption="""Amir Rahmati
                            Assistant professor, Stony Brook University""")
            self.sender.sendMessage(text="""Incorporating security at the inception of a technology is a goal we frequently strive for, but rarely achieve. Most of the research in the security domain is reactive: We design attacks, defenses, and systems to expose and fix vulnerabilities...
                        http://wss.ce.sharif.edu/seminar/165/""", reply_markup=day1_morning_keyboard)

        if msg["text"] == day1_morning_buttons_texts[6]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/3d/e0/3de08e1db4db7211d021ce52a706a838.jpg",
                caption="""Ali Eslami
            Staff Research Scientist, Google DeepMind""")
            self.sender.sendMessage(text=""" Scene representation—the process of converting visual sensory data into concise descriptions—is a requirement for intelligent behavior. Recent work has shown that neural networks excel at this task when provided with large, labeled datasets...
            http://wss.ce.sharif.edu/seminar/148/""", reply_markup=day1_morning_keyboard)



            # self.sender.sendMessage(text="ارایه مورد نظر را مشخص کنید.", reply_markup=day1_morning_keyboard)

    def day1_afternoon_speech_handler(self, msg):
        # self.sender.sendMessage(text="ارایه مورد نظر را مشخص کنید.", reply_markup=day1_afternoon_keyboard)
        if msg["text"] == day1_afternoon_buttons_texts[0]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/67/8e/678e6147ccfb1dbf4c18d117c1c03b4f.jpg",
                caption="""Mohammad Ghavamzadeh
            Senior Researcher, Google DeepMind""")
            self.sender.sendMessage(text="""In many practical problems from online advertisement to health informatics and computational finance, it is often important to be able to guarantee that the policy/strategy generated by our algorithm performs at least as well as a baseline. This reduces the risk of deploying our policy and helps us to convince the product (hospital, investment) manager that it is not going to harm the business….
            http://wss.ce.sharif.edu/seminar/88/""", reply_markup=day1_afternoon_keyboard)

        if msg["text"] == day1_afternoon_buttons_texts[1]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/48/20/4820c78100847f837281226e351682bb.jpg",
                caption="""Ali Sharifi Zarchi
            Research Associate, Colorado State University, Fort Collins""")
            self.sender.sendMessage(text="""During past decades, a major framework of bioinformatics has been an integration between algorithmic and statistical methods. For example, an analysis pipeline for Next Generation Sequencing (NGS) data might consist of some algorithmic pre-processing methods, such as alignment of the reads to a reference genome, followed by statistical post-processing methods, such as…
            http://wss.ce.sharif.edu/seminar/119/""", reply_markup=day1_afternoon_keyboard)

        if msg["text"] == day1_afternoon_buttons_texts[2]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/3a/5c/3a5c34c58fe24e6c26aaad02bdc0e02b.jpg",
                caption="""Arsalan Mohsen Nia
            Postdoc. Research Associate, Princeton University / Purdue University""")
            self.sender.sendMessage(text="""Most computer systems authenticate users only once at the time of initial login, which can lead to security concerns. Continuous authentication has been explored as an approach for alleviating such concerns. Previous methods for continuous authentication primarily use biometrics, e.g., fingerprint…
            http://wss.ce.sharif.edu/seminar/73/""", reply_markup=day1_afternoon_keyboard)

        if msg["text"] == day1_afternoon_buttons_texts[3]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/e6/11/e61125c63244091b3657b260ad859b5f.jpg",
                caption="""Niloofar Salehi
            Ph.D. Student, Stanford University, Computer Science department""")
            self.sender.sendMessage(text="""Distributed, parallel crowd workers can accomplish simple tasks through workflows, but teams of collaborating crowd workers are necessary for complex goals. Unfortunately, a fundamental condition for effective teams — familiarity with other members — stands in contrast to crowd work’s flexible...
            http://wss.ce.sharif.edu/seminar/74/""", reply_markup=day1_afternoon_keyboard)

        if msg["text"] == day1_afternoon_buttons_texts[4]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/46/33/46331a8cb75452a402623e7ca8c81639.jpg",
                caption="""Sahar Harati
            Ph.D. Student, Emory University""")
            self.sender.sendMessage(text="""We used several metrics of variability to extract unsupervised features from video recordings of patients before and after deep brain stimulation (DBS) treatment for major depressive disorder (MDD). Our goal was to quantify the treatment effects on facial expressivity. Multiscale entropy (MSE)…
            http://wss.ce.sharif.edu/seminar/89/""", reply_markup=day1_afternoon_keyboard)

        if msg["text"] == day1_afternoon_buttons_texts[5]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/1a/e4/1ae40fba26bbf2661eccfeb23575272f.jpg",
                caption="""Seyed Hossein Mortazavi
                        Ph.D. student, University of Toronto""")
            self.sender.sendMessage(text="""Path computing is a new paradigm that generalizes the edge computing vision into a multi-tier cloud architecture deployed over the geographic span of the network. Path computing supports scalable and localized processing by providing storage and computation along a succession of…
                        http://wss.ce.sharif.edu/seminar/87/""", reply_markup=day1_afternoon_keyboard)

        if msg["text"] == day1_afternoon_buttons_texts[6]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/f4/13/f41380422521276bd2f63f5cdc213627.jpg",
                caption="""Farzaneh Mirzazadeh
            Postdoc. research scientist, MIT-IBM Watson AI lab""")
            self.sender.sendMessage(text="""Co-embedding is the process of mapping elements from multiple sets into a common latent space, which can be exploited to infer element-wise associations by considering the geometric proximity of their embeddings. Such an approach underlies the state of the art for link prediction,…
            http://wss.ce.sharif.edu/seminar/99/""", reply_markup=day1_afternoon_keyboard)

    # todo num 0 is empty
    def day2_morning_speech_handler(self, msg):
        if msg["text"] == day2_morning_buttons_texts[0]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/04/b1/04b1f33a40160dc8d78ac2b5c00d64a1.jpg",
                caption="""Mohammad Mahdian
                            Staff Research Scientist, Google Research""")
            self.sender.sendMessage(text="http://wss.ce.sharif.edu/seminar/135/", reply_markup=day2_morning_keyboard)
        if msg["text"] == day2_morning_buttons_texts[1]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/21/39/213907a1d261a655ad40dd83f5496c18.jpg",
                caption="""Mahdi Jafari Siavoshani
            Assistant Professor, Sharif University of Technology""")
            self.sender.sendMessage(text="""In this presentation, we talk about "information theoretic secrecy" in general and the problem of secret key agreement among multiple parties in the presence of an eavesdropper in particular. The notion of information theoretic secrecy is much stronger than the classical approach in cryptography which is mainly based on unproven assumptions about computational hardness of some problems. This means…
            http://wss.ce.sharif.edu/seminar/80/""", reply_markup=day2_morning_keyboard)
        if msg["text"] == day2_morning_buttons_texts[2]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/1a/d7/1ad74ea64a51913dd5d4e1c3a6dd896b.jpg",
                caption="""Rouhollah Mahfouzi
                            Ph.D. Student, Linköping University""")
            self.sender.sendMessage(text="""Real-time communication over Ethernet is becoming important in various application areas of cyber-physical systems such as industrial automation and control, avionics, and automotive networking. Since such applications are typically time critical, Ethernet technology has been enhanced to support time-driven communication through the IEEE 802.1 TSN standards…
                        http://wss.ce.sharif.edu/seminar/80/""", reply_markup=day2_morning_keyboard)
        if msg["text"] == day2_morning_buttons_texts[3]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/25/5f/255f017c481c456088557872331011e0.jpg",
                caption="""Mostafa Rezazad
            Postdoctoral Researcher, Singapore University of Technology and Design""")
            self.sender.sendMessage(text="""Crossfire attack is a recently proposed threat designed to disconnect whole geographical areas, such as cities or states, from the Internet. Orchestrated in multiple phases, the attack uses a massively distributed botnet to generate low-rate benign traffic aiming to congest selected network links,...
             http://wss.ce.sharif.edu/seminar/79/""", reply_markup=day2_morning_keyboard)

        if msg["text"] == day2_morning_buttons_texts[4]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/1a/c8/1ac8a32db963424f4a4e659a0254b8d8.jpg",
                caption="""Salman Abolfath Beygi
            Associate Professor, IPM""")
            self.sender.sendMessage(text="""Non-locality is the phenomenon of observing strong correlations among the outcomes of local measurements of a multipartite physical system (particularly in quantum systems). No-signaling boxes are the abstract objects for studying non-locality,…
            http://wss.ce.sharif.edu/seminar/82/""", reply_markup=day2_morning_keyboard)

        if msg["text"] == day2_morning_buttons_texts[5]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/83/f8/83f86209855c831dbf02d21bf11d5b5a.jpg",
                caption="""Hadi Daneshmand
            Ph.D. Student, ETH Zurich""")
            self.sender.sendMessage(text="""The emerge of "big data" has created a need for computationally-statistically efficient optimization methods. From a statistical point of view, more observations are more information in that one can invoke asymptotical results. However, the computational complexity of learning methods…
            http://wss.ce.sharif.edu/seminar/83/""", reply_markup=day2_morning_keyboard)

        if msg["text"] == day2_morning_buttons_texts[6]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/f6/75/f675d4f85183434d50a594a3ab348b2f.jpg",
                caption="""Mohammad Amin Fazli
            Assistant Professor, Sharif University of Technology""")
            self.sender.sendMessage(text="""Social norms are a core concept in social sciences and play a critical role in regulating a society’s behaviors. Organizations and even governmental bodies use this social component to tackle varying challenges in society, as it is a less costly alternative to establishing...
            http://wss.ce.sharif.edu/seminar/106/""", reply_markup=day2_morning_keyboard)

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
                photo="http://wss.ce.sharif.edu/media/cache/f6/af/f6afcf31b1e5a420413715e9a5c0db75.jpg",
                caption="""Taha Yasseri
                            Associate Professor, University of Oxford""")
            self.sender.sendMessage(text="""We are nowadays at a crossroads, at which new approaches converge to tackle old problems in the study of social systems. We name such crossroads computational social science (CSS) : a new discipline that can offer abstracted (simplified, idealized) models and methods (mainly from statistical physics), large storage, algorithms and computational power (computer and data science), and a set of social hypotheses together with a…
                                http://wss.ce.sharif.edu/seminar/85/""", reply_markup=day2_afternoon_keyboard)
        if msg["text"] == day2_afternoon_buttons_texts[1]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/8a/81/8a81f2341826aa959146341522e49bbc.jpg",
                caption="""Hamid Bagheri
                    Assistant Professor, Nebraska-Lincoln""")
            self.sender.sendMessage(text="""The ever-increasing expansion of software into nearly every aspect of modern life, from mobile banking to healthcare systems, is making its dependability more important than ever. Software verification is known to provide the highest degree of software…
                    http://wss.ce.sharif.edu/seminar/86/""", reply_markup=day2_afternoon_keyboard)

        if msg["text"] == day2_afternoon_buttons_texts[2]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/0e/8a/0e8a2d32b0e5e8bf341743ad4f1a27b5.jpg",
                caption="""Behnam Bahrak
                            Assistant Professor, University of Tehran""")
            self.sender.sendMessage(text="""Mobile phones are ubiquitous. In many countries, including Iran, the coverage reaches 100% of the population, and even in remote villages, it is not unusual to cross paths with someone in the street talking on a mobile phone. Due to their ubiquity, mobile phones have the potential to be used as millions of sensors of their environment and provide us with an extremely rich and informative source of data.…
                                http://wss.ce.sharif.edu/seminar/122/""", reply_markup=day2_afternoon_keyboard)

        if msg["text"] == day2_afternoon_buttons_texts[3]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/05/ba/05bab14e4dc61c764c4e41a08c9bb81b.jpg",
                caption="""Mohammad Mahmoody
                    Assistant Professor, University of Virginia""")
            self.sender.sendMessage(text="""In this work, we revisit and extend the bitwise tampering model of Austrin et al. to the blockwise setting where each incoming block of randomness becomes tamperable with independent probability p. Our main result is an efficient blockwise p-tampering attack to bias the average of any efficient function…
                    http://wss.ce.sharif.edu/seminar/101/""", reply_markup=day2_afternoon_keyboard)

        if msg["text"] == day2_afternoon_buttons_texts[4]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/b6/e2/b6e2fc19e103cd183dc16e1b4eae0894.jpg",
                caption="""Mohammadreza Karimi
                            Master Student, ETH Zürich""")
            self.sender.sendMessage(text="""Stochastic optimization of continuous objectives is at the heart of mod- ern machine learning. However, many important problems are of discrete nature and often involve submodular objectives. We seek to unleash the power of stochastic continuous optimization, namely stochastic gradient descent and its variants, to such discrete problems. We first introduce the problem of stochastic submodular optimization,…
                    http://wss.ce.sharif.edu/seminar/118/""", reply_markup=day2_afternoon_keyboard)

        if msg["text"] == day2_afternoon_buttons_texts[5]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/38/be/38be94f77a0e85c6b7187c430ccd7ea6.jpg",
                caption="""Saba Ahmadian
                    Ph.D. student, Sharif University of Technology""")
            self.sender.sendMessage(text=""""With increasing performance requirements of data-intensive applications in data centers, storage subsystems have become performance bottlenecks of computing systems. Hard Disk Drives (HDDs), which are used as main media to store user data in storage systems, provide large capacity and low cost, ..
                    http://wss.ce.sharif.edu/seminar/77/""", reply_markup=day2_afternoon_keyboard)

        if msg["text"] == day2_afternoon_buttons_texts[6]:
            self.sender.sendPhoto(
                photo="http://wss.ce.sharif.edu/media/cache/27/00/2700d6ddcc88f0114f7454cd47215d06.jpg",
                caption="""Mehrdad Bakhtiari
                            Ph.D. Student, University of California San Diego""")
            self.sender.sendMessage(text=""""Methods to identify signatures of selective sweeps in population genomics data have been actively developed, but most do not identify the specific mutation favored by the selective sweep. We present a method, iSAFE, that uses a statistic derived solely from population genetics signals to pinpoint the favored mutation even when the signature of selection extends to 5Mbp..
                                http://wss.ce.sharif.edu/seminar/117/""", reply_markup=day2_afternoon_keyboard)

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
                   day1_afternoon_buttons_texts[6]: day1_afternoon_speech_handler,
                   day1_afternoon_buttons_texts[7]: previous,

                   day2_morning_buttons_texts[0]: day2_morning_speech_handler,
                   day2_morning_buttons_texts[1]: day2_morning_speech_handler,
                   day2_morning_buttons_texts[2]: day2_morning_speech_handler,
                   day2_morning_buttons_texts[3]: day2_morning_speech_handler,
                   day2_morning_buttons_texts[4]: day2_morning_speech_handler,
                   day2_morning_buttons_texts[5]: day2_morning_speech_handler,
                   day2_morning_buttons_texts[6]: day2_morning_speech_handler,
                   day2_morning_buttons_texts[7]: previous,


                   day2_afternoon_buttons_texts[0]: day2_afternoon_speech_handler,
                   day2_afternoon_buttons_texts[1]: day2_afternoon_speech_handler,
                   day2_afternoon_buttons_texts[2]: day2_afternoon_speech_handler,
                   day2_afternoon_buttons_texts[3]: day2_afternoon_speech_handler,
                   day2_afternoon_buttons_texts[4]: day2_afternoon_speech_handler,
                   day2_afternoon_buttons_texts[5]: day2_afternoon_speech_handler,
                   day2_afternoon_buttons_texts[6]: day2_afternoon_speech_handler,
                   day2_afternoon_buttons_texts[7]: previous,

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
