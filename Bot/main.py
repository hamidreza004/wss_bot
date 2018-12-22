import telepot
import sqlite3
from telepot.loop import MessageLoop
import datetime
from telepot.delegate import pave_event_space, per_chat_id, create_open
import os.path

TOKEN = None

try:
    token_file_path = os.path.join(os.path.dirname(__file__), "TOKEN.txt")
    print()
    with open(token_file_path, 'r') as token_file:
        TOKEN = token_file.readline().strip()
except:
    print("Token file doesn't exist.")


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


bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, StateHandler, timeout=2 * 24 * 60 * 60),  # timeout = 2 days?
])
start_time_ms = datetime.datetime

MessageLoop(bot).run_forever()
