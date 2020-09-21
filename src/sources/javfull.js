const { JSDOM } = require('jsdom');
const utils = require('./utils');
const ds = require('../ds');

const requester = utils.requester('https://javfull.net');

const searchByCode = async (code) => {
  let html = null;
  try {
    const rsp = await requester.get(`/?s=${encodeURI(code)}`);
    html = rsp.data;
  } catch (err) {
    html = err.response.data;
  }
  const dom = new JSDOM(html, { resources: 'usable', runScripts: 'dangerously' });
  const item = dom.window.document.querySelector('.item');
  if (!item) {
    return null;
  }
  const av = new ds.AV();
  av.code = code;
  av.preview_img_url = utils.noexcept(() => item.querySelector('img').src);
  av.video_url = utils.noexcept(() => item.querySelector('a').href);
  return av;
};

module.exports = {
  searchByCode,
};
