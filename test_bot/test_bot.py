# encoding: utf-8

import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from app.server import search, get_brief, get_magnet, get_new
try:
    import typing
except ImportError:
    typing = None
    pass
import requests
import urllib3
from utils.node import Node
import pytest


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
Node.start_node()


def test_search_by_code():
    for code in ("ABP-231", "ABP-123", "SSNI-351"):
        mock_message = MockMessage(mock_user, mock_chat.id, "/search")
        mock_update = MockUpdate(mock_message)
        search(mock_bot, mock_update, [code])
        received = mock_user.look_received()
        assert len(received) == 1
        assert requests.get(received[0]["photo"], verify=False).status_code == 200
        assert requests.get(received[0]["reply_markup"]["inline_keyboard"][0][0]['url'],
                            verify=False).status_code == 200


def test_search_by_actress():
    mock_message = MockMessage(mock_user, mock_chat.id, "/search")
    mock_update = MockUpdate(mock_message)
    search(mock_bot, mock_update, [u"桃乃木かな"])
    received = mock_user.look_received()
    assert len(received) > 0
    readable = 0

    for res in received:
        if requests.get(res["photo"], verify=False).status_code == 200:
            readable += 1

    assert readable > 0


def test_brief():
    for code in ("ABP-231", "ABP-123", "SSNI-351"):
        mock_message = MockMessage(mock_user, mock_chat.id, "/brief")
        mock_update = MockUpdate(mock_message)
        get_brief(mock_bot, mock_update, [code])
        received = mock_user.look_received()
        assert len(received) == 1
        assert requests.get(received[0]["photo"], verify=False).status_code == 200


def test_magnet():
    for code in ("ABP-231", "ABP-123", "SSNI-351"):
        mock_message = MockMessage(mock_user, mock_chat.id, "/magnet")
        mock_update = MockUpdate(mock_message)
        get_magnet(mock_bot, mock_update, [code])
        received = mock_user.look_received()
        assert len(received) > 0


def test_new():
    mock_message = MockMessage(mock_user, mock_chat.id, "/new")
    mock_update = MockUpdate(mock_message)
    get_new(mock_bot, mock_update, ["0", "20"])
    received = mock_user.look_received()
    assert len(received) > 0
    for res in received:
        assert requests.get(res["photo"], verify=False).status_code == 200


def test_end():
    Node.kill_node()
    exit(0)
