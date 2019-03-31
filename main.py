# encoding: utf-8

from utils.node import Node
from app.webserver import app

# start node.js subprocess
Node.start_node()

# # run telegram bot service
# run()

# run web server
app.app.run('0.0.0.0', 8081)
