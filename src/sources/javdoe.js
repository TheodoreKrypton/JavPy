const utils = require('./utils');
const ds = require('../ds');
const { JSDOM } = require('jsdom');

const requester = utils.requester('https://javdoe.tv');

const searchByCode = async (code) => {
  const rsp = await requester.get(encodeURI(`/search.html?q=${code}`));
  console.log(rsp.data);
  const dom = new JSDOM(rsp.data, { runScripts: 'dangerously' }).window.document;
  const player = dom.querySelector('#player');
  console.log(player.innerHTML);

};

module.exports = {
  searchByCode,
};


(async () => {
  console.log(await searchByCode('040911_068'));
})();