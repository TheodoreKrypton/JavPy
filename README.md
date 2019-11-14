![banner](https://i.imgur.com/KjqLjdA.png)
## Quick Start

### With pip
```bash
$ pip install JavPy
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

open http://localhost:8081 in explorer and enjoy driving!
```

Indicator|Status
:---: | :---:
Ubuntu & Mac OS | ![Build Status](https://github.com/TheodoreKrypton/JavPy/workflows/JavPy%20Build%20Test/badge.svg)
Windows | [![Build Status](https://theodorekrypton.visualstudio.com/JavPy/_apis/build/status/JavPy-Windows?branchName=master)](https://theodorekrypton.visualstudio.com/JavPy/_build/latest?definitionId=3&branchName=master)
Coverage | [![codecov](https://codecov.io/gh/TheodoreKrypton/JavPy/branch/master/graph/badge.svg)](https://codecov.io/gh/TheodoreKrypton/JavPy)
pypi |[![Python Version](https://img.shields.io/pypi/pyversions/JavPy.svg)](https://pypi.org/project/JavPy/) [![Latest Version](https://pypip.in/version/JavPy/badge.svg?text=version)](https://pypi.python.org/pypi/JavPy/) [![Downloads](https://pypip.in/download/JavPy/badge.svg)](https://pypi.python.org/pypi/JavPy/) [![Wheel Status](https://pypip.in/wheel/JavPy/badge.svg)](https://pypi.python.org/pypi/JavPy/)
Docker | [![Auto Docker Build](https://img.shields.io/docker/cloud/automated/wheatcarrier/javpy)](https://hub.docker.com/r/wheatcarrier/javpy) [![Docker Build](https://img.shields.io/docker/cloud/build/wheatcarrier/javpy)](https://hub.docker.com/r/wheatcarrier/javpy) [![Docker Pull](https://img.shields.io/docker/pulls/wheatcarrier/javpy)](https://hub.docker.com/r/wheatcarrier/javpy)
Discussion | [![Telegram Chat](https://img.shields.io/badge/JavPy-telegram%20chat-blue?style=social&logo=telegram)](https://t.me/JavPyGroup)

This project will continue supporting Python2 until it retire in 2020.

## 简介/Introduction

这是一个用来搜索日本 AV 相关信息的 Python 库，目前提供 2 种用户接口，一个为移动设备服务的 telegram bot，和一个为桌面个人电脑服务的 web 页面。

这个 Python 库从多个网站爬取信息，但多数目标网站在一些特定地区都被禁止访问。为了更好的使用体验，建议将这个库运行在互联网管制较少的地区，如美国，日本等。

总而言之，有三个要点：

1.  **这个库用来搜索日本 AV**
2.  **这个库提供两个接口：telegram bot 和 web**
3.  **如果网络环境不好，请使用 VPN**

---

This is a Python library for searching related information of Japanese AVs. This project temporarily provide 2 kind of interfaces, a telegram bot for mobile users and a locally hosted web page for PC users.

This library fetches information from various websites, but most of them are blocked in some regions. To experience a better travel, please host the service in somewhere having lesser Internet restrictions, like the USA, Japan, etc.

**In brief, there are 3 main instructions concluded below.**

1.  **It is for searching Japanese AVs.**
2.  **It provides 2 interfaces: telegram bot and web.**
3.  **Use VPN if you experience network issues.**

## Web

![](preview.png)

### Attention!
**本项目将会在2020年开始永久停止支持Python2版本**

----

**This project will permanently end support for Python 2 in 2020.**

**0.2.5 注意：如果你将服务部署在一个远程机器**，像是云虚拟专用服务器上，你可能会担心网站被其他未经许可的人访问。在**0.2.5**发布版后，JavPy会自动创建一个配置文件`~/.JavPy/config.json`。你可以**将你的私人ip或ip段**添加到文件中，或者直接**创建一个密码**。未被认证的访问将被拦截并得到一个400错误响应。你也可以在页面右上角的设置按钮配置选项。

----

**0.2.5 Note: If you want to run the server on a remote machine** like cloud VPS, you may be worry about the website being accessed by unauthorised people. After release **0.2.5**, JavPy will automatically create a configuration file  `~/.JavPy/config.json` on its first run. You can **add your personal IPs or IP ranges** into the file or just **create a password**. Unauthorised access will then be blocked and get a response of Error 400. You can also set the configuration with the settings button on the top right of tha web page.

### Developer Guide
Backend:
```bash
pip install -r requirements.txt
python main.py
```

Frontend:
```
cd app/web
npm install
npm run serve
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
-   install node.js

```bash
curl -sL https://deb.nodesource.com/setup_10.x | bash -
apt-get install nodejs -y
```

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

