const { JSDOM } = require('jsdom');
const utils = require('./utils');
const ds = require('../ds');
const { Magnet } = require('../ds');

const requester = utils.requester('https://javdb.com');
const regexes = {
  volume: new RegExp(/\d+(\.\d+)[MG]B/),
};

const urlCache = {};

const getUrl = async (code) => {
  if (urlCache[code] === undefined) {
    const rsp = await requester.get(`/videos/search_autocomplete.json?q=${encodeURI(code)}`);
    if (rsp.data.length === 0 || !rsp.data[0].title.toLowerCase().includes(code.toLowerCase())) {
      urlCache[code] = null;
    } else {
      urlCache[code] = `/v/${rsp.data[0].uid}`;
    }
  }
  return urlCache[code];
};

const getBrief = async (code) => {
  const url = await getUrl(code);
  if (url === null) {
    return null;
  }
  const rsp = await requester.get(url);
  const dom = new JSDOM(rsp.data).window.document;
  const brief = new ds.AV();
  brief.preview_img_url = dom.querySelector('img.video-cover').src;
  brief.title = dom.querySelector('.title').textContent.trim();

  dom.querySelectorAll('.panel-block').forEach((div) => {
    const strong = div.querySelector('strong');
    if (!strong) {
      return;
    }
    const key = strong.textContent.trim();
    switch (key) {
      case '番號:': {
        brief.code = div.querySelector('.value').textContent.trim();
        break;
      }
      case '時間:': {
        brief.release_date = div.querySelector('.value').textContent.trim();
        break;
      }
      case '演員:': {
        const actresses = div.querySelector('.value').textContent.trim();
        if (actresses !== 'N/A') {
          brief.actress = actresses.split(',').map((actress) => actress.trim());
        }
        break;
      }
      default: {
        break;
      }
    }
  });

  return brief;
};

const searchMagnet = async (code) => {
  const url = await getUrl(code);
  if (url === null) {
    return null;
  }
  const rsp = await requester.get(url);
  const dom = new JSDOM(rsp.data).window.document;
  return [...dom.querySelector('#magnets-content').querySelectorAll('a')].map((a) => {
    const magnet = new Magnet();
    magnet.magnet = a.href;
    magnet.description = utils.noexcept(() => a.querySelector('.meta').textContent.match(regexes.volume)[0]);
    return magnet;
  });
};

const getNewlyReleased = async (page) => {
  const censoredUrl = `/?page=${page}&vft=0`;
  const uncensoredUrl = `/uncensored?page=${page}&vft=0`;

  return (await Promise.allSettled([censoredUrl, uncensoredUrl].map(
    (url) => requester.get(url).then((rsp) => {
      const dom = new JSDOM(rsp.data).window.document;
      return [...dom.querySelector('#videos').querySelectorAll('.grid-item')].map((video) => {
        const av = new ds.AV();
        av.title = video.querySelector('.video-title').textContent.trim();
        av.code = video.querySelector('.uid').textContent.trim();
        av.release_date = video.querySelector('.meta').textContent.trim();
        av.preview_img_url = utils.noexcept(() => video.querySelector('img').getAttribute('data-src'));
        return av;
      });
    }).catch(() => []),
  ))).reduce((a, b) => a.value.concat(b.value));
};

module.exports = {
  getBrief,
  searchMagnet,
  getNewlyReleased,
};
