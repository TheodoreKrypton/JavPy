from sources.javmost_com import JavMostCom
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

src = JavMostCom()
print src.search("KAWD-654")