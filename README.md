<div align=center>

![logo](https://github.com/TheodoreKrypton/JavPy/raw/master/JavPy/app/web/src/assets/logo.png)

![](https://travis-ci.org/TheodoreKrypton/JavPy.svg?branch=master)
[![Build Status](https://theodorekrypton.visualstudio.com/main/_apis/build/status/TheodoreKrypton.JavPy?branchName=master)](https://theodorekrypton.visualstudio.com/main/_build/latest?definitionId=1&branchName=master)

[![codecov](https://codecov.io/gh/TheodoreKrypton/JavPy/branch/master/graph/badge.svg)](https://codecov.io/gh/TheodoreKrypton/JavPy)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/2a42b438eade46ae897a727068621ace)](https://www.codacy.com/app/TheodoreKrypton/JavPy?utm_source=github.com&utm_medium=referral&utm_content=TheodoreKrypton/JavPy&utm_campaign=Badge_Coverage)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d64d4e093e204f5dbf668a4fcc87dceb)](https://app.codacy.com/app/TheodoreKrypton/JavPy?utm_source=github.com&utm_medium=referral&utm_content=TheodoreKrypton/JavPy&utm_campaign=Badge_Grade_Dashboard)
[![codebeat badge](https://codebeat.co/badges/08449fa3-5997-4b6b-8549-147d144f829d)](https://codebeat.co/projects/github-com-theodorekrypton-javpy-master)
![](https://sonarcloud.io/api/project_badges/measure?project=TheodoreKrypton_JavPy&metric=alert_status)

[![Python Version](https://img.shields.io/pypi/pyversions/JavPy.svg)](https://pypi.org/project/JavPy/)
[![Latest Version](https://pypip.in/version/JavPy/badge.svg?text=version)](https://pypi.python.org/pypi/JavPy/)
[![Downloads](https://pypip.in/download/JavPy/badge.svg)](https://pypi.python.org/pypi/JavPy/)
[![Wheel Status](https://pypip.in/wheel/JavPy/badge.svg)](https://pypi.python.org/pypi/JavPy/)

</div>

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

### User Guide

```bash
pip install JavPy
```
```pythonconsole
# in python console
>>> import JavPy
>>> JavPy.serve()
```

Open [http://localhost:8081](http://localhost:8081) and enjoy driving!

### Developer Guide

```bash
pip install -r requirements.txt
python main.py
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
-   Place your bot token into the "token.txt"
-   install node.js

```bash
curl -sL https://deb.nodesource.com/setup_10.x | bash -
apt-get install nodejs -y
```

-   install libtorrent

```bash
apt-get install python-libtorrent
```

-   run `python main.py`

------------------

<div align=center>


*Acknowledgements*

*This project does not include any stored or static data, and all the data it presents are collected realtime and automatically from the websites below. Internet data are public but messy and collecting them is a tiring work. Appreciate them for their offering precious and high quality data.*

[JavMost](https://www5.javmost.com)  [AVSOX](https://avsox.net)  [AV女優名 変換君](http://etigoya955.blog49.fc2.com/)  [IndexAV](https://indexav.com)  [JavBus](https://www.javbus.com)  [xopenload.video](https://www.xopenload.video)  [YouAV](https://www.xopenload.video)  [Avgle](https://avgle.com)  [Fembed](https://www.fembed.com)

</div>