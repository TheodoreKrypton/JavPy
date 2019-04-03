# encoding: utf-8

from __future__ import absolute_import, print_function, unicode_literals
from JavPy.utils.node import Node
from JavPy.app.webserver import app


# start node.js subprocess
# Node.start_node()

# # run telegram bot service
# run()

# run web server
app.app.run('0.0.0.0', 8081)
