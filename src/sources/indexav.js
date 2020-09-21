const { JSDOM } = require('jsdom');
const utils = require('./utils');
const ds = require('../ds');

const requester = utils.requester('https://indexav.com');

const getInfoFromCard = (card) => {
  const av = new ds.AV();
  av.code = card.querySelector('.tag.is-link.is-light').textContent.trim();
  av.actress = [...card.querySelectorAll('.tag.is-primary.is-light')].map((tag) => tag.textContent.trim());
  const h5 = card.querySelector('.title');
  av.title = h5.textContent.trim();
  av.preview_img_url = h5.querySelector('a').rel;
  av.release_date = utils.noexcept(() => card.querySelector('footer > p').textContent.trim());
  return av;
};

const searchByActressInPage = async (actress, n) => {
  const rsp = await requester.get(`/actor/${encodeURI(actress)}?page=${n}`);
  const dom = new JSDOM(rsp.data);
  return [...dom.window.document.querySelectorAll('.video_column')].map(getInfoFromCard);
};

const searchByActress = async (actress) => {
  const rsp = await requester.get(`/actor/${encodeURI(actress)}`);
  const dom = new JSDOM(rsp.data);
  const ul = dom.window.document.querySelector('.pagination-list');
  if (!ul) {
    return searchByActressInPage(actress, 1);
  }
  return [...ul.querySelectorAll('li')].map((li) => {
    const page = li.textContent.trim();
    return searchByActressInPage(actress, page);
  });
};

const getBrief = async (code) => {
  const rsp = await requester.get(`/search?keyword=${encodeURI(code)}`);
  const dom = new JSDOM(rsp.data);
  const card = dom.window.document.querySelector('.card');
  if (!card) {
    return null;
  }

  if (card.textContent.includes('Sad, cannot find any video in database')) {
    return null;
  }
  return getInfoFromCard(card);
};

module.exports = {
  searchByActress,
  getBrief,
};
