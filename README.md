![banner](https://i.imgur.com/KjqLjdA.png)
## Quick Start

**Make sure you've installed nodejs first**

* Linux, Mac OS:
```bash
$ curl -sL https://deb.nodesource.com/setup_10.x | bash -
$ apt-get install nodejs -y
```

* Windows:
https://nodejs.org/en/download/

### With pip
```bash
$ pip install JavPy

# or download the JavPy whl release in the release page
$ pip install JavPy-x.x.x-py2.py3-none-any.whl
```

then
```bash
$ javpy
```
or alternatively,
```bash
$ python -c "import JavPy; JavPy.serve()"
```

and wait up to 5 secs

### With Docker
```bash
$ docker pull wheatcarrier/javpy:latest
```
then
```bash
$ docker run -p 8081:8081 wheatcarrier/javpy:latest
```
open http://localhost:8081 in explorer and enjoy driving!

### With Git
```bash
$ git clone https://github.com/TheodoreKrypton/JavPy.git
$ cd JavPy
$ python3 setup.py install
$ javpy
```
and wait up to 5 secs to start driving

Indicator|Status
:---: | :---:
Ubuntu & Mac OS | ![Build Status](https://github.com/TheodoreKrypton/JavPy/workflows/JavPy%20Build%20Test/badge.svg)
Windows | [![Build Status](https://theodorekrypton.visualstudio.com/JavPy/_apis/build/status/JavPy-Windows?branchName=master)](https://theodorekrypton.visualstudio.com/JavPy/_build/latest?definitionId=3&branchName=master)
Coverage | [![codecov](https://codecov.io/gh/TheodoreKrypton/JavPy/branch/master/graph/badge.svg)](https://codecov.io/gh/TheodoreKrypton/JavPy)
pypi |[![Python Version](https://img.shields.io/pypi/pyversions/JavPy.svg)](https://pypi.org/project/JavPy/) [![Latest Version](https://pypip.in/version/JavPy/badge.svg?text=version)](https://pypi.python.org/pypi/JavPy/) [![Downloads](https://pypip.in/download/JavPy/badge.svg)](https://pypi.python.org/pypi/JavPy/) [![Wheel Status](https://pypip.in/wheel/JavPy/badge.svg)](https://pypi.python.org/pypi/JavPy/)
Docker | [![Auto Docker Build](https://img.shields.io/docker/cloud/automated/wheatcarrier/javpy)](https://hub.docker.com/r/wheatcarrier/javpy) [![Docker Build](https://img.shields.io/docker/cloud/build/wheatcarrier/javpy)](https://hub.docker.com/r/wheatcarrier/javpy) [![Docker Pull](https://img.shields.io/docker/pulls/wheatcarrier/javpy)](https://hub.docker.com/r/wheatcarrier/javpy)
Discussion | [![Telegram Chat](https://img.shields.io/badge/JavPy-telegram%20chat-blue?style=social&logo=telegram)](https://t.me/JavPyGroup) 

## 简介/Introduction

这是一个用来搜索日本 AV 相关信息的 Python 库，目前提供 2 种用户接口，一个为移动设备服务的 telegram bot，和一个为桌面个人电脑服务的 web 页面。

这个 Python 库从多个网站爬取信息，但多数目标网站在一些特定地区都被禁止访问。为了更好的使用体验，建议将这个库运行在互联网管制较少的地区，如美国，日本等。

总而言之，有三个要点：

1.  **这个库用来搜索日本 AV**
2.  **这个库提供两个接口：telegram bot 和 web**
3.  **如果网络环境不好，请使用 VPN**

---

This is a Python library for searching Japanese AVs related information. This project temporarily provides both a telegram bot and a locally hosted web page, correspondingly for mobile users and for PC users as interfaces.

This library fetches information from various websites, but most of them are blocked in some regions. To experience a better travel, please host the service in somewhere having lesser Internet restrictions, like the USA, Japan, etc.

**In brief, there are 3 main instructions concluded below.**

1.  **It is for searching Japanese AVs.**
2.  **It provides 2 interfaces: telegram bot and web.**
3.  **Use VPN if you experience network issues.**

## Web

![](preview.png)

### Configuration
#### `ip-whitelist` and `password`

**如果你将服务部署在一个远程机器**，像是云虚拟专用服务器上，你可能会担心网站被其他未经许可的人访问。在**0.2.5**发布版后，JavPy会自动创建一个配置文件`~/.JavPy/config.json`。你可以**将你的私人ip或ip段**添加到文件中，并**创建一个密码**。未被认证的访问将被拦截并得到一个400错误响应。你也可以在页面右上角的设置按钮配置选项。

----

**If you want to run the server on a remote machine** like a cloud VPS, you may be worry about the website being accessed by unauthorised people. After release **0.2.5**, JavPy will automatically create a configuration file  `~/.JavPy/config.json` on its first run. You can **add your personal IPs or IP ranges** into the file and **create a password**. Unauthorised access will then be blocked and get a response of Error 400. You can also set the configuration with the settings button on the top right of tha web page.

#### `proxy`

如果你需要使用代理，请在`~/.JavPy/config.json`中设置`proxy`这一项，目前可以支持socks5与http代理

例子：`proxy: "http://127.0.0.1:1080"`

----

If you need to use a proxy, simply set the `proxy` field in the `~/.JavPy/config.json`. Currently both socks5 and http proxies are supported.

Example: `proxy: "http://127.0.0.1:1080"`

### Contributor Guide
```bash
$ git clone https://github.com/TheodoreKrypton/JavPy.git
```

Backend:
```bash
$ pip3 install -r requirements.txt
$ python3 main.py
```

Frontend:
```bash
$ cd JavPy/app/web
$ npm install
```
Modify the port to 8081 in `config.js` when debugging and make sure you have recovered it before releasing. 

```bash
$ npm run serve
```

## Telegram Bot

### Demo

[https://t.me/JavExpert_bot](https://t.me/JavExpert_bot) (TEMPORARILY SHUTDOWN)

### Supported Commands

-   /start guided jav trip
-   /search \[code\]
-   /search \[actress name\] --many-actresses \[allow/denied\] -upto 20
-   /new \[--many-actresses\] \[allow/denied\] -upto 20
-   /brief \[code\]
-   /magnet \[code\]

### Quick Start

-   Go to the telegram bot father and apply for a bot token
-   Clone this repo and create a new file named "token.txt"
-   Copy your bot token into the "token.txt"

```python
from JavPy.app.tgbot.server import run

run(open("token.txt").read())
```

------------------

<div align=center>


*Acknowledgements*

*This project does not include any stored or static data, and all the data it presents are collected realtime and automatically from the websites below. Internet data are public but messy and collecting them is a tiring work. Appreciate them for their offering precious and high quality data.*

[JavMost](https://www5.javmost.com)  [AVSOX](https://avsox.net)  [AV女優名 変換君](http://etigoya955.blog49.fc2.com/)  [IndexAV](https://indexav.com)  [JavBus](https://www.javbus.com)  [xopenload.video](https://www.xopenload.video)  [YouAV](https://www.xopenload.video)  [Avgle](https://avgle.com)  [Fembed](https://www.fembed.com) [素人系AV女優大辞典wiki](https://av-help.memo.wiki/) [JavModel](https://javmodel.com/) [Warashi Asian Pornstars Database](http://warashi-asian-pornstars.fr/en/s-0/wapdb-database-of-asian-pornstars-japanese-av-actresses-and-actors) [JavFull.net](https://javfull.net/) [JavLibrary](http://www.javlibrary.com) [XFantasy](https://https://xfantasy.tv)

</div>

