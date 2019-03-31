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

## Introduction

This is a Python library for searching related information of Japanese AVs. This project temporarily provide 2 kind of interfaces, a telegram bot for mobile users and a locally hosted web page for PC users.

For both previewing and my testing need, there is a demo for the telegram bot hosted on a really tiny cloud server. Please don't rely on it for the server overloading concerns. If you like it, please clone this repo and host it on your own server.

This library fetches information from various websites, but most of them are blocked in some regions. To experience a better travel, please host the service in somewhere having lesser Internet restrictions, like the USA, Japan, etc.

**In brief, there are 4 main instructions concluded below.**

1. **It is for searching Japanese AVs.**
2. **It provides 2 interfaces: telegram bot and web.**
3. **Don't rely on the bot presented below. It is hosted on a tiny cloud server.**
4. **Use VPN if you experience network issues.**

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
