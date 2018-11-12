import urllib3
from app.server import run

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

run()
