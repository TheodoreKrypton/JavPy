![](https://travis-ci.org/TheodoreKrypton/JavPy.svg?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d64d4e093e204f5dbf668a4fcc87dceb)](https://app.codacy.com/app/TheodoreKrypton/JavPy?utm_source=github.com&utm_medium=referral&utm_content=TheodoreKrypton/JavPy&utm_campaign=Badge_Grade_Dashboard)
[![codebeat badge](https://codebeat.co/badges/08449fa3-5997-4b6b-8549-147d144f829d)](https://codebeat.co/projects/github-com-theodorekrypton-javpy-master)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/TheodoreKrypton/JavPy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/TheodoreKrypton/JavPy/alerts/)
[![Language grade: JavaScript](https://img.shields.io/lgtm/grade/javascript/g/TheodoreKrypton/JavPy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/TheodoreKrypton/JavPy/context:javascript)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/TheodoreKrypton/JavPy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/TheodoreKrypton/JavPy/context:python)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)
[![Maintainability](https://api.codeclimate.com/v1/badges/7854ab72a6692d85b865/maintainability)](https://codeclimate.com/github/TheodoreKrypton/JavPy/maintainability)


![](https://sonarcloud.io/api/project_badges/quality_gate?project=TheodoreKrypton_JavPy)
# JavPy 
A python library for searching usable url of japanese AV according to given code

## Telegram Bot
[https://t.me/JavExpert_bot](https://t.me/JavExpert_bot)

### Supported Commands
* /start guided jav trip
* /search \[code\]
* /search \[actress name\] --many-actresses \[allow/denied\] -upto 20
* /new \[--many-actresses\] \[allow/denied\] -upto 20
* /brief \[code\]
* /magnet \[code\]

## TODO

* [ ] daily recommendations
* [ ] top viewed
* [x] usable magnet link
* [ ] name translation (jp-zh-en)
* [ ] uncensored videos
* [ ] ambiguous search

## Quick Start
* Go to the telegram bot father and apply for a bot token
* Clone this repo and create a new file named "token.txt"
* Place your bot token into the "token.txt"
* install node.js 
    ```bash
    curl -sL https://deb.nodesource.com/setup_10.x | bash -
    apt-get install nodejs -y
    ```
* install libtorrent
    ```angular2html
    apt-get install python-libtorrent
    ```
* run `python main.py`
