const { JSDOM } = require('jsdom');
const utils = require('./utils');
const ds = require('../ds');

const requester = utils.requester('https://www2.javhdporn.net');

const regexes = {
  embedUrl: new RegExp(/"embedURL":"(.+?)"/),
};

const searchByCode = async (code) => {
  const rsp = await requester.get(`/?s=${encodeURI(code)}`);
  const dom = new JSDOM(rsp.data).window.document;
  const main = dom.querySelector('main');
  if (main.querySelector('.widget-title')) {
    return null;
  }
  const articles = dom.querySelectorAll('article');
  let url = null;
  const av = new ds.AV();

  for (let i = 0; i < articles.length; i += 1) {
    const div = articles[i];
    const title = utils.noexcept(() => div.querySelector('header').textContent);
    if (utils.titleIncludes(title, code)) {
      url = div.querySelector('a').href;
      av.preview_img_url = utils.noexcept(() => div.querySelector('img').src);
      av.title = title.trim();
      av.code = code;
      break;
    }
  }

  if (url === null) {
    return null;
  }

  const rsp2 = await requester.get(url);
  const dom2 = new JSDOM(rsp2.data).window.document;

  av.video_url = utils.noexcept(() => dom2.querySelector('.yoast-schema-graph').textContent.match(regexes.embedUrl)[1]);
  if (!av.video_url) {
    return null;
  }

  av.actress = [...dom2.querySelector('#video-actors').querySelectorAll('a')].map((a) => a.textContent.trim());
  return av;
};

module.exports = {
  searchByCode,
};
