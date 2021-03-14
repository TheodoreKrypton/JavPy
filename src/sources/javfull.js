const { JSDOM } = require('jsdom');
const utils = require('./utils');
const ds = require('../ds');

const requester = utils.requester('https://javfull.net');

const searchByCode = async (code) => {
  const rsp = await requester.get(`/${code}/`);
  const html = rsp.data;
  const dom = new JSDOM(html).window.document;
  const av = new ds.AV();
  av.title = utils.noexcept(() => dom.querySelector('h1').textContent);
  av.code = code;
  av.preview_img_url = utils.noexcept(() => dom.querySelector('.iframeplayer').getAttribute('data-bg').match(/url\('(.+?)'\)/)[1]);
  av.video_url = `https://javfull.net/${code}/`;
  return av;
};

module.exports = {
  searchByCode,
};
