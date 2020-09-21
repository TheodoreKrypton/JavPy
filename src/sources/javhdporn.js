const { JSDOM } = require('jsdom');
const utils = require('./utils');
const ds = require('../ds');

const requester = utils.requester('https://www2.javhdporn.net');

const regexes = {
  embedUrl: new RegExp(/"embedURL":"(.+?)"/),
};

const searchByCode = async (code) => {
  const rsp = await requester.get(`/?s=${encodeURI(code)}`);
  const dom = new JSDOM(rsp.data);
  const main = dom.window.document.querySelector('main');
  if (main.querySelector('.widget-title')) {
    return null;
  }
  const div = dom.window.document.querySelector('article');

  const av = new ds.AV();
  av.preview_img_url = utils.noexcept(() => div.querySelector('img').src);
  av.code = code;

  const url = div.querySelector('a').href;
  const rsp2 = await requester.get(url);
  const dom2 = new JSDOM(rsp2.data);

  av.title = utils.noexcept(() => dom2.window.document.querySelector('h1').textContent);
  if (!av.title.includes(code)) {
    return null;
  }

  av.video_url = utils.noexcept(() => dom2.window.document.querySelector('.yoast-schema-graph').textContent.match(regexes.embedUrl)[1]);
  if (!av.video_url) {
    return null;
  }

  av.actress = [...dom2.window.document.querySelector('#video-actors').querySelectorAll('a')].map((a) => a.textContent.trim());
  return av;
};

module.exports = {
  searchByCode,
};
