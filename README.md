# JavPy

![Github Actions](https://github.com/TheodoreKrypton/javpy/workflows/test/badge.svg)
![codecov](https://codecov.io/gh/TheodoreKrypton/javpy/branch/master/graph/badge.svg)
![npm](https://img.shields.io/npm/v/javpy)

![](preview.png)

## Contents

* [Introduction](#简介introduction)
* [Quick Start](#quick-start)
* [Configurations](#Configurations)
* [Acknowledgements](#Acknowledgements)

## 简介/Introduction

这是一个用来搜索日本 AV 相关信息的 NodeJS App，目前提供一个基于WebSocket的Web客户端页面。

这个App从多个网站爬取信息，但多数目标网站在一些特定地区都被禁止访问。为了更好的使用体验，建议将这个库运行在互联网管制较少的地区，如美国，日本等。


---

This is a NodeJS App for searching Japanese AVs related information. This project temporarily only provides a WebSocket based web page as interface.

This App fetches information from various websites, but most of them are blocked in some regions. To experience a better travel, please host the service in somewhere having lesser Internet restrictions, like the USA, Japan, etc.

## Quick Start

### With Prebuilt Binaries
* Simply go to [Releases](https://github.com/TheodoreKrypton/JavPy/releases), download an executable and just run and enjoy.

### With Git
```bash
$ git clone https://github.com/TheodoreKrypton/javpy
$ cd javpy && npm install -g --only=prod
$ javpy --port 8081
```

### With npm
```bash
$ npm install -g --only=prod javpy
$ javpy --port 8081
```

### With Docker
```bash
$ docker run -p 8081:8081 wheatcarrier/javpy:latest
```

## Configurations
### `ip-whitelist` and `password`

**如果你将服务部署在一个远程机器**，像是云虚拟专用服务器上，你可能会担心网站被其他未经许可的人访问。JavPy会自动创建一个配置文件`~/.JavPy/config.json`。你可以**将你的私人ip或ip段**添加到文件中，并**创建一个密码**。未被认证的访问将被拦截并得到一个400错误响应。你也可以在页面左上角的设置按钮配置选项。

----

**If you want to run the server on a remote machine** like a cloud VPS, you may be worry about the website being accessed by unauthorised people. JavPy will automatically create a configuration file  `~/.JavPy/config.json` on its first run. You can **add your personal IPs or IP ranges** into the file and **create a password**. Unauthorised access will then be blocked and get a response of Error 400. You can also set the configuration with the settings button on the top left of tha web page.

### `proxy`

如果你需要使用代理，请在`~/.JavPy/config.json`中设置`proxy`这一项，目前可以支持socks5与http代理

例子：`proxy: "http://127.0.0.1:1080"`

----

If you need to use a proxy, simply set the `proxy` field in the `~/.JavPy/config.json`. Currently both socks5 and http proxies are supported.

Example: `proxy: "http://127.0.0.1:1080"`


**注意：**若使用docker进行服务，请务必记得在退出docker前将config文件保存，不管是通过`docker cp`进行备份或通过`docker commit`提交修改。

**Attention:** If you are serving with docker, please don't forget to save your config file before exiting the container. You can either backup the config file with `docker cp` or save your changes into an image with `docker commit`.

------------------

<div align=center id="Acknowledgements">



*Acknowledgements*

*This project does not include any stored or static data, and all the data it presents are collected realtime and automatically from the websites below. Internet data are public but messy and collecting them is a tiring work. Appreciate them for their offering precious and high quality data.*

[JavMost](https://www5.javmost.com)  [AVSOX](https://avsox.net)  [AV女優名 変換君](http://etigoya955.blog49.fc2.com/)  [IndexAV](https://indexav.com)  [JavBus](https://www.javbus.com)  [xopenload.video](https://www.xopenload.video)  [YouAV](https://www.xopenload.video)  [Avgle](https://avgle.com)  [Fembed](https://www.fembed.com) [素人系AV女優大辞典wiki](https://av-help.memo.wiki/) [JavModel](https://javmodel.com/) [Warashi Asian Pornstars Database](http://warashi-asian-pornstars.fr/en/s-0/wapdb-database-of-asian-pornstars-japanese-av-actresses-and-actors) [JavFull.net](https://javfull.net/) [JavLibrary](http://www.javlibrary.com) [XFantasy](https://https://xfantasy.tv)

</div>