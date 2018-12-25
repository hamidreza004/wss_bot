# coding: utf-8
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from farsi_texts import *

from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


def _create_default_keyboard():
    # return ReplyKeyboardMarkup(keyboard=[KeyboardButton(text=keyboard_text) for keyboard_text in default_buttons_texts])
    temp = list(map(lambda text: KeyboardButton(text=text), default_buttons_texts))
    btn_lst = [
        [
            temp[0], temp[1], temp[2]
        ],
        [
            temp[3], temp[4], temp[5]
        ],
        [
            temp[6]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _location_default_keyboard():
    loc_temp = list(map(lambda text: KeyboardButton(text=text), locations_buttons_texts))
    btn_lst = [
        [
            loc_temp[0]
        ],
        [
            loc_temp[2], loc_temp[3]
        ],
        [
            loc_temp[4]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _sponsor_default_keyboard():
    spon_temp = list(map(lambda text: KeyboardButton(text=text), sponsor_buttons_texts))
    btn_lst = [
        [
            spon_temp[0]
        ],
        [
            spon_temp[1]
        ],
        [
            spon_temp[2]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _contact_us_keyboard():
    contactUs_temp = list(map(lambda text: KeyboardButton(text=text), contact_us_buttons_text))
    btn_lst = [
        [
            contactUs_temp[0]
        ],
        [
            contactUs_temp[1]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _contact_us_keyboard1():
    contactUs_temp = list(map(lambda text: KeyboardButton(text=text), contact_us_buttons_text1))
    btn_lst = [
        [
            contactUs_temp[0]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)



def _days_keyboard():
    days = list(map(lambda text: KeyboardButton(text=text), days_buttons_texts))
    btn_lst = [
        [
            days[0]
        ],
        [
            days[1]
        ],
        [
            days[2]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _day1_keyboard():
    day1 = list(map(lambda text: KeyboardButton(text=text), day1_buttons_texts))
    btn_lst = [
        [
            day1[0]
        ],
        [
            day1[1]
        ],
        [
            day1[2]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _day2_keyboard():
    day2 = list(map(lambda text: KeyboardButton(text=text), day2_buttons_texts))
    btn_lst = [
        [
            day2[0]
        ],
        [
            day2[1]
        ],
        [
            day2[2]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _day1_morning_keyboard():
    day1_morn = list(map(lambda text: KeyboardButton(text=text), day1_morning_buttons_texts))
    btn_lst = [
        [
            day1_morn[0]
        ],
        [
            day1_morn[1]
        ],
        [
            day1_morn[2]
        ],
        [
            day1_morn[3]
        ],
        [
            day1_morn[4]
        ],
        [
            day1_morn[5]
        ],
        [
            day1_morn[6]
        ],
        [
            day1_morn[7]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _day1_afternoon_keyboard():
    day1_after = list(map(lambda text: KeyboardButton(text=text), day1_afternoon_buttons_texts))
    btn_lst = [
        [
            day1_after[0]
        ],
        [
            day1_after[1]
        ],
        [
            day1_after[2]
        ],
        [
            day1_after[3]
        ],
        [
            day1_after[4]
        ],
        [
            day1_after[5]
        ],
        [
            day1_after[6]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _day2_morning_keyboard():
    day2_morn = list(map(lambda text: KeyboardButton(text=text), day2_morning_buttons_texts))
    btn_lst = [
        [
            day2_morn[0]
        ],
        [
            day2_morn[1]
        ],
        [
            day2_morn[2]
        ],
        [
            day2_morn[3]
        ],
        [
            day2_morn[4]
        ],
        [
            day2_morn[5]
        ],
        [
            day2_morn[6]
        ],
        [
            day2_morn[7]
        ],
        [
            day2_morn[8]
        ],
        [
            day2_morn[9]
        ]

    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _day2_afternoon_keyboard():
    day2_after = list(map(lambda text: KeyboardButton(text=text), day2_afternoon_buttons_texts))
    btn_lst = [
        [
            day2_after[0]
        ],
        [
            day2_after[1]
        ],
        [
            day2_after[2]
        ],
        [
            day2_after[3]
        ],
        [
            day2_after[4]
        ],
        [
            day2_after[5]
        ],
        [
            day2_after[6]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _read_keyboard():
    read = list(map(lambda text: KeyboardButton(text=text), read_text))
    btn_lst = [
        [
            read[0]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _day1_morning_poll_keyboard():
    day1_morn = list(map(lambda text: KeyboardButton(text=text), day1_morning_poll_buttons_texts))
    btn_lst = [
        [
            day1_morn[0]
        ],
        [
            day1_morn[1]
        ],
        [
            day1_morn[2]
        ],
        [
            day1_morn[3]
        ],
        [
            day1_morn[4]
        ],
        [
            day1_morn[5]
        ],
        [
            day1_morn[6]
        ],
        [
            day1_morn[7]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _day1_afternoon_poll_keyboard():
    day1_after = list(map(lambda text: KeyboardButton(text=text), day1_afternoon_poll_buttons_texts))
    btn_lst = [
        [
            day1_after[0]
        ],
        [
            day1_after[1]
        ],
        [
            day1_after[2]
        ],
        [
            day1_after[3]
        ],
        [
            day1_after[4]
        ],
        [
            day1_after[5]
        ],
        [
            day1_after[6]
        ],
        [
            day1_after[7]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _day2_morning_poll_keyboard():
    day2_morn = list(map(lambda text: KeyboardButton(text=text), day2_morning_poll_buttons_texts))
    btn_lst = [
        [
            day2_morn[0]
        ],
        [
            day2_morn[1]
        ],
        [
            day2_morn[2]
        ],
        [
            day2_morn[3]
        ],
        [
            day2_morn[4]
        ],
        [
            day2_morn[5]
        ],
        [
            day2_morn[6]
        ],
        [
            day2_morn[7]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _day2_afternoon_poll_keyboard():
    day2_after = list(map(lambda text: KeyboardButton(text=text), day2_afternoon_poll_buttons_texts))
    btn_lst = [
        [
            day2_after[0]
        ],
        [
            day2_after[1]
        ],
        [
            day2_after[2]
        ],
        [
            day2_after[3]
        ],
        [
            day2_after[4]
        ],
        [
            day2_after[5]
        ],
        [
            day2_after[6]
        ],
        [
            day2_after[7]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _poll_keyboard():
    poll = list(map(lambda text: KeyboardButton(text=text), poll_texts))
    btn_lst = [
        [
            poll[0]
        ],
        [
            poll[1]
        ],
        [
            poll[2]
        ],
        [
            poll[3]
        ],
        [
            poll[4]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _poll_first_afternoon_keyboard():
    poll = list(map(lambda text: KeyboardButton(text=text), poll_texts))
    btn_lst = [
        [
            poll[1]
        ],
        [
            poll[4]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _poll_second_morning_keyboard():
    poll = list(map(lambda text: KeyboardButton(text=text), poll_texts))
    btn_lst = [
        [
            poll[2]
        ],
        [
            poll[4]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _poll_second_afternoon_keyboard():
    poll = list(map(lambda text: KeyboardButton(text=text), poll_texts))
    btn_lst = [
        [
            poll[3]
        ],
        [
            poll[4]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _rate_keyboard():
    rate = list(map(lambda text: KeyboardButton(text=text), rate_text))
    btn_lst = [
        [
            rate[0]
        ],
        [
            rate[1]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)


def _rate_keyboard1():
    rate = list(map(lambda text: KeyboardButton(text=text), rate_text1))
    btn_lst = [
        [
            rate[0]
        ],
        [
            rate[1]
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=btn_lst)

default_keyboard = _create_default_keyboard()
sponsor_keyboard = _sponsor_default_keyboard()
location_keyboard = _location_default_keyboard()
days_keyboard = _days_keyboard()
day1_keyboard = _day1_keyboard()
day2_keyboard = _day2_keyboard()
day1_morning_keyboard = _day1_morning_keyboard()
day1_afternoon_keyboard = _day1_afternoon_keyboard()
day2_morning_keyboard = _day2_morning_keyboard()
day2_afternoon_keyboard = _day2_afternoon_keyboard()
contact_us_keyboard = _contact_us_keyboard()
contact_us_keyboard1 = _contact_us_keyboard1()
read_keyboard = _read_keyboard()
day1_morning_poll_keyboard = _day1_morning_poll_keyboard()
day1_afternoon_poll_keyboard = _day1_afternoon_poll_keyboard()
day2_morning_poll_keyboard = _day2_morning_poll_keyboard()
day2_afternoon_poll_keyboard = _day2_afternoon_poll_keyboard()
poll_keyboard = _poll_keyboard()
# poll_first_afternoon_keyborad = _poll_first_afternoon_keyboard()
# poll_second_morning_keyboard = _poll_second_morning_keyboard()
# poll_second_afternoon_keyboard = _poll_second_afternoon_keyboard()
rate_keyboard = _rate_keyboard()
rate_keyboard1 = _rate_keyboard1()