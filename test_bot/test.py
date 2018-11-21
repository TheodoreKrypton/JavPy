import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from app.server import search
try:
    import typing
except ImportError:
    typing = None
    pass
import requests
import urllib3
from utils import node

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class MockGlobals:
    def __init__(self):
        self.__chat_id = 0
        self.bot = None

    def get_chat_id(self):
        self.__chat_id += 1
        return self.__chat_id

    def register_bot(self, bot):
        self.bot = bot


class MockUser:
    def __init__(self, user_id):
        self.id = user_id
        self.__received_messages = []
        self.chats = {}  # type: typing.List[MockChat]

    def send_message(self, *args, **kwargs):
        self.chats[kwargs["chat_id"]].bot.receive_message(**kwargs)

    def receive_message(self, text):
        self.__received_messages.append(text)

    def look_received(self):
        ret = self.__received_messages[:]
        self.__received_messages = []
        return ret


class MockMessage:
    def __init__(self, user, chat_id, text):
        self.user = user
        self.chat_id = chat_id
        self.text = text


class MockChat:
    def __init__(self, user, bot):
        self.id = mock_globals.get_chat_id()
        self.user = user  # type: MockUser
        self.bot = bot  # type: MockBot
        self.user.chats[self.id] = self
        self.bot.chats[self.id] = self


class MockBot:
    def __init__(self):
        self.chats = {}  # type: typing.List[MockChat]
        self.__received_messages = []
        self.send_photo = self.send_message

    def send_message(self, *args, **kwargs):
        self.chats[kwargs["chat_id"]].user.receive_message(kwargs)

    def receive_message(self, message):
        self.__received_messages.append(message)


class MockUpdate:
    def __init__(self, message):
        self.message = message


mock_globals = MockGlobals()
mock_user = MockUser(0)
mock_bot = MockBot()
mock_chat = MockChat(mock_user, mock_bot)
node.start()


class TestClass:
    def test_search_by_code(self):
        mock_message = MockMessage(mock_user, mock_chat.id, "/search")
        mock_update = MockUpdate(mock_message)
        search(mock_bot, mock_update, ["ABP-231"])
        received = mock_user.look_received()
        assert len(received) == 1
        assert requests.get(received[0]["photo"], verify=False).status_code == 200
        # assert requests.get(received[0]["reply_markup"]["inline_keyboard"][0][0]['url'], verify=False).status_code == 200

    def test_end(self):
        node.kill_node()