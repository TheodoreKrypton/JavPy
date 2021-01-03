const { JSDOM } = require('jsdom');
const utils = require('./utils');
const ds = require('../ds');

const requester = utils.requester('https://javdoe.tv');

const searchByCode = async (code) => {
  const rsp = await requester.get(encodeURI(`/search.html?q=${code}`));
  const dom = new JSDOM(rsp.data, { runScripts: 'dangerously' }).window.document;
  const player = dom.querySelector('#player');
};

module.exports = {
  searchByCode,
};
