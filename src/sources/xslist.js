const FormData = require('form-data');
const { fs } = require('memfs');
const { JSDOM } = require('jsdom');
const utils = require('./utils');

const requester = utils.requester('https://xslist.org');

const searchActressByImage = async (image) => {
  const blob = Buffer.from(image.split(',')[1], 'base64');
  const fileName = `/${Math.random()}`;
  fs.writeFileSync(fileName, blob);
  const formData = new FormData();
  formData.append('pic', fs.createReadStream(fileName));
  const rsp = await requester.post('/search/pic', formData, { headers: formData.getHeaders() });
  const dom = new JSDOM(rsp.data).window.document;
  return [...dom.querySelectorAll('a')].map((a) => {
    const tokens = a.text.split('-');
    return tokens.length === 3 ? tokens[1].trim() : tokens[0].trim();
  });
};

module.exports = {
  searchActressByImage,
};
