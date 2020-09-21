const sources = require('../sources');
const utils = require('./utils');

const searchMagnet = async (ws, reqId, { code }) => {
  let something = false;
  await Promise.allSettled([sources.javbus, sources.javdb].map(
    (source) => source.searchMagnet(code).then((response) => {
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
  searchMagnet,
};
