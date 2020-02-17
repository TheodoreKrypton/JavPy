import requests
from JavPy.app.tgbot.server import (
    search,
    get_brief,
    get_magnet,
    get_new,
    start,
    Interactive,
)
from JavPy.utils.testing import *
from JavPy.utils.config import proxy


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
        self.chats = {}  # type: typing.Dict[int, MockChat]

    def send_message(self, *_, **kwargs):
        self.chats[kwargs["chat_id"]].bot.receive_message(**kwargs)

    def receive_message(self, text):
        self.__received_messages.append(text)

    def look_received(self):
        ret = self.__received_messages[:]
        self.__received_messages = []
        return ret


def generate_message_id():
    message_id = 0
    while True:
        yield message_id
        message_id += 1


class MockMessage:
    __generate_message_id = generate_message_id()

    def __init__(self, user, chat_id, text):
        self.from_user = user
        self.chat_id = chat_id
        self.text = text
        self.message_id = next(MockMessage.__generate_message_id)


mock_globals = MockGlobals()
mock_user = MockUser(0)


class MockChat:
    def __init__(self, user, bot):
        self.id = mock_globals.get_chat_id()
        self.user = user  # type: MockUser
        self.bot = bot  # type: MockBot
        self.user.chats[self.id] = self
        self.bot.chats[self.id] = self


class MockBot:
    def __init__(self):
        self.chats = {}  # type: typing.Dict[int, MockChat]
        self.__received_messages = []
        self.send_photo = self.send_message

    def send_message(self, *_, **kwargs):
        self.chats[kwargs["chat_id"]].user.receive_message(kwargs)

    def receive_message(self, message):
        self.__received_messages.append(message)


class MockUpdate:
    def __init__(self, message):
        self.message = message


mock_bot = MockBot()
mock_chat = MockChat(mock_user, mock_bot)


@testing(code=("JUY-805", "040219_01", "SSNI-351"))
def test_search_by_code(code):
    mock_message = MockMessage(mock_user, mock_chat.id, "/search")
    mock_update = MockUpdate(mock_message)
    search(mock_bot, mock_update, [code])
    received = mock_user.look_received()
    assert len(received) == 1
    assert requests.get(received[0]["photo"], proxies=proxy).status_code == 200
    assert (
        requests.get(
            received[0]["reply_markup"]["inline_keyboard"][0][0]["url"],
            proxies=proxy
        ).status_code
        == 200
    )


@testing(command=("ABP-123 -o".split(),))
def test_search_by_code_exception(command):
    mock_message = MockMessage(mock_user, mock_chat.id, "/search")
    mock_update = MockUpdate(mock_message)
    search(mock_bot, mock_update, command)
    received = mock_user.look_received()
    assert "Sorry, Wrong Usage" in received[0]["text"]


@testing(command=("桃乃木かな -m on -u 10".split(),))
def test_search_by_actress(command):
    mock_message = MockMessage(mock_user, mock_chat.id, "/search")
    mock_update = MockUpdate(mock_message)
    search(mock_bot, mock_update, command)
    received = mock_user.look_received()
    assert len(received) > 0
    for res in received:
        if requests.get(res["photo"], proxies=proxy).status_code == 200:
            return
    assert False


@testing(command=("桃乃木かな -m 1 -u 10a".split(), "桃乃木かな -n 1".split()))
def test_search_by_actress_exception(command):
    mock_message = MockMessage(mock_user, mock_chat.id, "/search")
    mock_update = MockUpdate(mock_message)
    search(mock_bot, mock_update, command)
    received = mock_user.look_received()
    print(received[0]["text"])
    assert "Search by name of an actress" in received[0]["text"]


@testing(code=("ABP-231", "ABP-123", "SSNI-351"))
def test_brief(code):
    mock_message = MockMessage(mock_user, mock_chat.id, "/brief")
    mock_update = MockUpdate(mock_message)
    get_brief(mock_bot, mock_update, [code])
    received = mock_user.look_received()
    assert len(received) == 1
    assert requests.get(received[0]["photo"], proxies=proxy).status_code == 200


@testing(code=("3408371-dirty-nun-fucks-the-gardener",))
def test_brief_without_img(code):
    mock_message = MockMessage(mock_user, mock_chat.id, "/brief")
    mock_update = MockUpdate(mock_message)
    get_brief(mock_bot, mock_update, [code])
    received = mock_user.look_received()
    assert len(received) == 1
    print(received)


@testing(
    command=("ABP-231 -a".split(), "ABP-231 -l jp".split(), "CRAZY-114514".split())
)
def test_brief_exception(command):
    mock_message = MockMessage(mock_user, mock_chat.id, "/brief")
    mock_update = MockUpdate(mock_message)
    get_brief(mock_bot, mock_update, [command])
    received = mock_user.look_received()
    assert "Sorry, No Video Found" in received[0]["text"]


@testing(code=("ABP-231", "ABP-123", "SSNI-351"))
def test_magnet(code):
    mock_message = MockMessage(mock_user, mock_chat.id, "/magnet")
    mock_update = MockUpdate(mock_message)
    get_magnet(mock_bot, mock_update, [code])
    received = mock_user.look_received()
    assert len(received) > 0


@testing(params=("-m 1 -u 20".split()))
def test_new(params):
    mock_message = MockMessage(mock_user, mock_chat.id, "/new")
    mock_update = MockUpdate(mock_message)
    get_new(mock_bot, mock_update, params)
    received = mock_user.look_received()
    for res in received:
        if requests.get(res["photo"], proxies=proxy).status_code == 200:
            return
    assert False


@testing(param=("-a 1 -b 20".split(), "-m 1 -u 10a".split()))
def test_new_exception(param):
    mock_message = MockMessage(mock_user, mock_chat.id, "/new")
    mock_update = MockUpdate(mock_message)
    get_new(mock_bot, mock_update, param)
    received = mock_user.look_received()
    assert "Get newly released videos" in received[0]["text"]


@testing()
def test_interactive():
    def interactive_assert(message, condition):
        interactive_mock_message = MockMessage(mock_user, mock_chat.id, message)
        interactive_mock_update = MockUpdate(interactive_mock_message)
        Interactive.message(mock_bot, interactive_mock_update)
        interactive_received = mock_user.look_received()
        assert condition(interactive_received)

    # test interactive start
    mock_message = MockMessage(mock_user, mock_chat.id, "/start")
    mock_update = MockUpdate(mock_message)
    start(mock_bot, mock_update)
    received = mock_user.look_received()
    assert len(received) == 1
    assert received[0]["text"] == "Hi, how can I help you?"

    # test interactive search by code
    interactive_assert(
        "Search",
        lambda rcv: len(rcv) == 1 and "Search a code or an actress." in rcv[0]["text"],
    )
    interactive_assert(
        "ABP-123",
        lambda rcv: len(rcv) == 1 and requests.get(rcv[0]["photo"], proxies=proxy).status_code == 200,
    )

    # test interactive search by actress
    interactive_assert(
        "Search",
        lambda rcv: len(rcv) == 1 and "Search a code or an actress." in rcv[0]["text"],
    )
    interactive_assert(
        "桃乃木かな",
        lambda rcv: len(rcv) == 1 and rcv[0]["text"] == "How many results? [Integer]",
    )
    interactive_assert(
        "5",
        lambda rcv: len(rcv) > 0
        and sum(map(lambda y: requests.get(y["photo"], proxies=proxy).status_code == 200, rcv)) > 0,
    )

    # test interactive search newly released
    interactive_assert(
        "New",
        lambda rcv: len(rcv) == 1 and "How many results? [Integer]" == rcv[0]["text"],
    )
    interactive_assert(
        "5",
        lambda rcv: len(rcv) > 0
        and sum(map(lambda y: requests.get(y["photo"], proxies=proxy).status_code == 200, rcv)) > 0,
    )

    # test interactive search random
    interactive_assert(
        "Random",
        lambda rcv: len(rcv) == 1 and "Search a code or an actress." in rcv[0]["text"],
    )

    # test interactive search magnets
    interactive_assert(
        "Magnet", lambda rcv: "Search a code. e.g. ABP-231" == rcv[0]["text"]
    )
    interactive_assert("ABP-123", lambda rcv: len(rcv) > 1)

    # test interactive search brief
    interactive_assert(
        "Brief", lambda rcv: "Search a code. e.g. ABP-231" == rcv[0]["text"]
    )
    interactive_assert(
        "ABP-123",
        lambda rcv: len(rcv) == 1 and requests.get(rcv[0]["photo"], proxies=proxy).status_code == 200,
    )


if __name__ == "__main__":
    test_search_by_code()
    test_search_by_code_exception()
    test_search_by_actress()
    test_search_by_actress_exception()
    test_brief()
    test_brief_without_img()
    test_brief_exception()
    test_magnet()
    test_new()
    test_new_exception()
    test_interactive()
