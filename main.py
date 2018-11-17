# encoding: utf-8

import urllib3
from app.server import run
from utils.node import start as start_node
import libtorrent


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# start node.js subprocess
start_node()

# run telegram bot service
run()
