const Axios = require('axios').default;
const { JSDOM } = require('jsdom');
const utils = require('./utils');
const ds = require('../ds');

const requester = utils.requester('https://avgo.me');

const searchByCode = async (code) => {
  const rsp = await requester.get(`/list/search/${code}`);
  const dom = new JSDOM(rsp.data).window.document;
  const div = dom.querySelector('.container-box').querySelectorAll('.border')[1];
  const desc = div.querySelector('.video-desc').textContent;

  if (!desc.toLowerCase().match(code.toLowerCase())) {
    return null;
  }

  const rsp2 = await requester.get(div.querySelector('a').href);
  console.log(rsp2.data);
  const dom2 = new JSDOM(rsp2.data).window.document;
  const buttons = dom2.querySelector('#video-group-btn').querySelectorAll('span');
  console.log([...buttons]);
};

module.exports = {
  searchByCode,
};
