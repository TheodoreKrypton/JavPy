import urllib3
from app.server import run
from utils.node import start as start_node


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

start_node()
run()
