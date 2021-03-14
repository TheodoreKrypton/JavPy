const jsdom = require('jsdom');
const { default: Axios } = require('axios');
const utils = require('./utils');
const ds = require('../ds');
const { noexcept } = require('./utils');

const { JSDOM } = jsdom;

const requester = utils.requester('https://www5.javmost.com');

const regexes = {
  code: new RegExp(/var YWRzNA = '(.+?)'/),
  code2: new RegExp(/var YWRzNQ = '(.+?)'/),
  code3: new RegExp(/var YWRzNg = '(.+?)'/),
  value: new RegExp(/var YWRzMQo = '(.+?)'/),
  sound: new RegExp(/'sound':'(.+?)'/),
  date: new RegExp(/\d\d\d\d-\d\d-\d\d/),
  quote: new RegExp(/'/g),
  params: new RegExp(/select_part\((.+?)\)/),
};

const tryOneButton = async (button, code, code2, code3, value, sound) => {
  const params = button.querySelector('a').getAttribute('onclick').match(regexes.params)[1];
  const tokens = params.split(',');
  const [part, group] = tokens.slice(0, 2).map((token) => token.replace(regexes.quote, ''));

  const data = `group=${group}&part=${part}&code=${code}&code2=${code2}&code3=${code3}&value=${value}&sound=${sound}`;
  const rsp = await requester.post('/ri3123o235r/', data, {
    headers: {
      'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    },
  });

  let url = rsp.data.data[0].trim();
  if (url.startsWith('//')) {
    url = `https:${url}`;
  }

  if (url.includes('avgle')) {
    if (await Axios.get(url).data.includes('This video is not available on this platform.')) {
      return null;
    }
  }

  if (url.endsWith('.m3u8') || url.endsWith('.mp4')) {
    return url;
  }

  if (await utils.testUrl(url)) {
    return url;
  }
  return null;
};

const searchByCode = async (code) => {
  const rsp = await requester.get(`/${code}/`);
  const dom = new JSDOM(rsp.data).window.document;

  let previewImgUrl = utils.noexcept(() => dom.querySelector('meta[property="og:image"]').content);

  const title = utils.noexcept(() => dom.querySelector('meta[property="og:description"]').content);

  const releaseDate = utils.noexcept(() => dom.querySelector('meta[property="video:release_date"]').content.slice(0, 10));

  const actress = [...dom.querySelectorAll('a.btn-danger:not(.btn-circle)')].map((button) => button.textContent);

  if (!previewImgUrl.startsWith('http:')) {
    previewImgUrl = `http:${previewImgUrl}`;
  }
  let buttons = [...dom.querySelector('.tab-overflow').querySelectorAll('li')];
  buttons = buttons.slice(1, buttons.length - 1);
  const sound = rsp.data.match(regexes.sound)[1];

  const scripts = [...dom.querySelectorAll('script')];
  const script = scripts[scripts.length - 5].innerHTML;
  const [_code, code2, code3, value] = ['code', 'code2', 'code3', 'value'].map((key) => encodeURIComponent(script.match(regexes[key])[1]));
  return buttons.map((button) => (async () => {
    const url = await tryOneButton(button, _code, code2, code3, value, sound);
    if (url) {
      const av = new ds.AV();
      av.preview_img_url = previewImgUrl;
      av.video_url = url;
      av.code = code;
      av.title = title;
      av.release_date = releaseDate;
      av.actress = actress;
      return av;
    }
    return null;
  })());
};

const getNewlyReleased = async (page) => {
  const rsp = await requester.get(`/showlist/new/${page}/release`);
  if (!rsp || !rsp.data) {
    return [];
  }
  const html = rsp.data.data;
  const dom = new JSDOM(html);
  return [...dom.window.document.querySelectorAll('.card')].map((card) => {
    const releaseDate = noexcept(() => card.textContent.match(regexes.date)[0]);
    const actress = [...card.querySelectorAll('.btn-danger')].map((button) => button.textContent);
    let previewImgUrl = noexcept(() => card.querySelector('img').getAttribute('data-src'));
    if (!previewImgUrl.startsWith('http')) {
      previewImgUrl = `http:${previewImgUrl}`;
    }
    const av = new ds.AV();
    av.preview_img_url = previewImgUrl;
    av.title = noexcept(() => card.querySelector('h5').textContent.trim());
    av.actress = actress;
    av.release_date = releaseDate;
    av.code = card.querySelector('h4').textContent.trim();
    return av;
  });
};

module.exports = {
  searchByCode,
  getNewlyReleased,
};
