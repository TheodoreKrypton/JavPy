const { JSDOM } = require('jsdom');
const utils = require('./utils');
const ds = require('../ds');

const requester = utils.requester('https://highporn.net');

const searchByCode = async (code) => {
  const rsp = await requester.get(`/search/videos?search_query=${encodeURI(code.toLowerCase())}`);
  if (rsp.data.includes('No Videos Found.')) {
    return null;
  }
  const dom = new JSDOM(rsp.data);
  const div = dom.window.document.querySelector('.well-sm');
  if (!div) {
    return null;
  }
  const av = new ds.AV();
  av.code = code;
  av.preview_img_url = utils.noexcept(() => div.querySelector('img').src);
  if (av.preview_img_url && !av.preview_img_url.startsWith('http')) {
    av.preview_img_url = `http:${av.preview_img_url}`;
  }
  av.title = utils.noexcept(() => div.querySelector('.video-title').textContent);
  av.video_url = utils.noexcept(() => div.querySelector('a').href);
  return av;
};

module.exports = {
  searchByCode,
};
