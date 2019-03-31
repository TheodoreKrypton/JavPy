<div align=center>

![](app/web/src/assets/logo.png)

![](https://travis-ci.org/TheodoreKrypton/JavPy.svg?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d64d4e093e204f5dbf668a4fcc87dceb)](https://app.codacy.com/app/TheodoreKrypton/JavPy?utm_source=github.com&utm_medium=referral&utm_content=TheodoreKrypton/JavPy&utm_campaign=Badge_Grade_Dashboard)
[![codebeat badge](https://codebeat.co/badges/08449fa3-5997-4b6b-8549-147d144f829d)](https://codebeat.co/projects/github-com-theodorekrypton-javpy-master)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/TheodoreKrypton/JavPy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/TheodoreKrypton/JavPy/alerts/)
[![Language grade: JavaScript](https://img.shields.io/lgtm/grade/javascript/g/TheodoreKrypton/JavPy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/TheodoreKrypton/JavPy/context:javascript)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/TheodoreKrypton/JavPy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/TheodoreKrypton/JavPy/context:python)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)
![](https://sonarcloud.io/api/project_badges/measure?project=TheodoreKrypton_JavPy&metric=alert_status)
</div>

## 简介/Introduction
这是一个用来搜索日本AV相关信息的Python库，目前提供2种用户接口，一个为移动设备服务的telegram bot，和一个为桌面个人电脑服务的web页面。

这个Python库从多个网站爬取信息，但多数目标网站在一些特定地区都被禁止访问。为了更好的使用体验，建议将这个库运行在互联网管制较少的地区，如美国，日本等。

总而言之，有三个要点：
1. **这个库用来搜索日本AV**
2. **这个库提供两个接口：telegram bot和web**
3. **如果网络环境不好，请使用VPN**

-----------------

This is a Python library for searching related information of Japanese AVs. This project temporarily provide 2 kind of interfaces, a telegram bot for mobile users and a locally hosted web page for PC users.

This library fetches information from various websites, but most of them are blocked in some regions. To experience a better travel, please host the service in somewhere having lesser Internet restrictions, like the USA, Japan, etc.

**In brief, there are 3 main instructions concluded below.**

1. **It is for searching Japanese AVs.**
2. **It provides 2 interfaces: telegram bot and web.**
3. **Use VPN if you experience network issues.**

## Web

![](preview.png)

### User Guide
```
pip install JavPy
(in Python console)
>>> import JavPy
>>> JavPy.serve()
```
Open http://localhost:8081 and enjoy driving!


### Developer Guide
```
pip install -r requirements.txt
python main.py
cd app/web
npm install
npm run serve
```

## Telegram Bot
### Demo

[https://t.me/JavExpert_bot](https://t.me/JavExpert_bot)  (TEMPORARILY SHUTDOWN)

### Supported Commands
* /start guided jav trip
* /search \[code\]
* /search \[actress name\] --many-actresses \[allow/denied\] -upto 20
* /new \[--many-actresses\] \[allow/denied\] -upto 20
* /brief \[code\]
* /magnet \[code\]

### Quick Start

- Go to the telegram bot father and apply for a bot token

- Clone this repo and create a new file named "token.txt"

- Place your bot token into the "token.txt"

- install node.js 

  ```bash
  curl -sL https://deb.nodesource.com/setup_10.x | bash -
  apt-get install nodejs -y
  ```

- install libtorrent

  ```bash
  apt-get install python-libtorrent
  ```

- run `python main.py`

## TODO

* [x] daily recommendations
* [ ] top viewed
* [x] usable magnet link
* [ ] name translation (jp-zh-en)
* [ ] uncensored videos
* [ ] ambiguous search
