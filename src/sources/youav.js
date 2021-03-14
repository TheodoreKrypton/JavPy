const { JSDOM } = require('jsdom');
const utils = require('./utils');
const ds = require('../ds');

const requester = utils.requester('https://www.youav.com');

const regexes = {
  pid: new RegExp(/var video_id = "(\d+)"/),
  button: new RegExp(/<button id="btn(\d+)"/),
  m3u8: new RegExp(/file: "(.+?)"/),
};

const button2server = {
  1: 7,
  2: 8,
  3: 2,
  101: 2,
  7: 4,
};

const decode = async (url) => {
  const rsp = await requester.get(encodeURI(url));
  const pid = rsp.data.match(regexes.pid)[1];
  const button = parseInt(rsp.data.match(regexes.button)[1], 10);
  let server = null;
  if (button2server[button] !== undefined) {
    server = button2server[button];
  } else {
    server = button;
  }
  const rsp2 = await requester.get(`/ajax/hls.php?server=${server}&pid=${pid}`);

  if (rsp2.data.startsWith('http')) {
    return rsp2.data;
  }
  return rsp2.data.match(regexes.m3u8)[1];
};

const searchByCode = async (code) => {
  const rsp = await requester.get(`/search/videos/${encodeURI(code)}`);
  const dom = new JSDOM(rsp.data);

  try {
    const divs = dom.window.document.querySelectorAll('div.content-row');
    const div = divs[divs.length - 1].querySelector('div');
    if (!div) {
      return null;
    }
    const av = new ds.AV();
    av.preview_img_url = div.querySelector('img').src;
    av.video_url = await decode(`${div.querySelector('a').href}`);
    av.code = code;
    av.title = div.querySelector('.content-title').textContent;
    return av;
  } catch {
    return null;
  }
};

module.exports = {
  searchByCode,
};
