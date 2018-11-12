import requests
import bs4
import re
import os

code = "IENE-623"
url = "https://www.xopenload.video/search.php?s=" + code
rsp = requests.get(url, verify=False)
bs = bs4.BeautifulSoup(rsp.text, "lxml")


div = bs.find(name='div', attrs={'class': 'poster'})

img = div.a.img.attrs['src']
url = div.a.attrs['href']


rsp = requests.get(url, verify=False)
_hash = re.search("https://www\.xopenload\.video/links\.php\?hash=(.+?)\"", rsp.text).group(1)
url = "https://www.xopenload.video/links.php?hash=" + _hash
rsp = requests.get(url, verify=False)
js = re.search("<script language=\"javascript\">(.+?)</script>", rsp.text, re.S).group(1)


js = js.replace("document", "console")
js = js.replace("write", "log")

f = open("tmp.js", "w")
f.write(js)
f.close()

output = os.popen("nodejs tmp.js", 'r')
res = output.read()
url = re.findall("https://.+?\"", res)[0][:-1]
print url