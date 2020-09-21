const { JSDOM } = require('jsdom');
const utils = require('./utils');
const ds = require('../ds');
const { AV } = require('../ds');

const requester = utils.requester('http://www.javlibrary.com');
const regexes = {
  video: new RegExp(/<div class="video".+?<\/div><\/div>/g),
  url: new RegExp(/"og:url" content="\/\/.+?(\/.+?)">/),
};

const getNewlyReleased = async (page) => {
  const [majors, dates] = await Promise.all([
    requester.get(`/ja/vl_newrelease.php?&mode=2&page=${page}`),
    requester.get(`/ja/vl_newrelease.php?list&mode=2&page=${page}`),
  ]);

  if (!majors) {
    return [];
  }

  const results = majors.data.match(regexes.video).map((video) => {
    const av = new ds.AV();
    const dom = new JSDOM(video).window.document;

    av.preview_img_url = utils.noexcept(() => dom.querySelector('img').src.replace('ps.jpg', 'pl.jpg'));
    if (av.preview_img_url && !av.preview_img_url.startsWith('http')) {
      av.preview_img_url = `http:${av.preview_img_url}`;
    }
    av.code = utils.noexcept(() => dom.querySelector('.id').textContent.trim());
    av.title = utils.noexcept(() => dom.querySelector('.title').textContent.trim());
    return av;
  });

  const dom = new JSDOM(dates.data).window.document;
  dom.querySelector('.videotextlist').querySelectorAll('tr:not(.header)').forEach((tr, i) => {
    results[i].release_date = tr.querySelectorAll('td')[1].textContent.trim();
  });

  return results;
};

const getBrief = async (code) => {
  let rsp = await requester.get(encodeURI(`/ja/vl_searchbyid.php?keyword=${code}`));
  if (!rsp) {
    return null;
  }
  let matched = rsp.data.match(regexes.url);
  if (!matched) {
    const dom = new JSDOM(rsp.data).window.document;
    rsp = await requester.get(`/ja${dom.querySelector('.video').querySelector('.a').href.slice(1)}`);
    matched = rsp.data.match(regexes.url);
    if (!matched) {
      return null;
    }
  }

  rsp = await requester.get(matched[1]);
  const html = rsp.data;
  const brief = new AV();
  const dom = new JSDOM(html).window.document;
  brief.title = dom.querySelector('.post-title').textContent;
  brief.preview_img_url = dom.querySelector('#video_jacket_img').src;
  if (!brief.preview_img_url.startsWith('http')) {
    brief.preview_img_url = `http:${brief.preview_img_url}`;
  }
  brief.code = code;
  const tds = dom.querySelector('#video_date').querySelectorAll('td');
  brief.date = tds[tds.length - 1].textContent;
  brief.actress = [...dom.querySelector('#video_cast').querySelectorAll('.star')].map((span) => span.textContent);
  return brief;
};

module.exports = {
  getNewlyReleased,
  getBrief,
};
