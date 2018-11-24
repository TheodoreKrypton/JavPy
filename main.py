# encoding: utf-8

import urllib3
from app.tgbot.server import run
from utils.node import Node


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# start node.js subprocess
Node.start_node()

# run telegram bot service
run()
