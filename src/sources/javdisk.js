const { JSDOM } = require('jsdom');
const utils = require('./utils');
const ds = require('../ds');

const requester = utils.requester('https://javdisk.com');

const searchByCode = async (code) => {
  const rsp = await requester.get(encodeURI(`/search.html?q=${code}`));
  const dom = new JSDOM(rsp.data).window.document;
  const av = new ds.AV();
  av.code = code;
  av.title = dom.querySelector('meta[property="og:title"]').content;
  if (!utils.titleIncludes(av.title, code)) {
    return null;
  }
  av.video_url = dom.querySelector('meta[property="og:url"]').content;
  av.preview_img_url = dom.querySelector('meta[property="og:image"]').content;
  return av;
};

module.exports = {
  searchByCode,
};
