const sources = require('../sources');
const utils = require('./utils');

const searchActressByImage = async (ws, reqId, { image }) => {
  let something = false;
  await Promise.allSettled([sources.xslist].map(
    (source) => source.searchActressByImage(image).then((response) => {
      if (!response) {
        return;
      }
      something = true;
      ws.send(JSON.stringify({ response, reqId }));
    }),
  ));
  if (!something) {
    utils.notFound(ws, reqId);
  }
};

module.exports = {
  searchActressByImage,
};
