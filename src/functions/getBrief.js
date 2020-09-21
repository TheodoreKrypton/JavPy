const sources = require('../sources');
const utils = require('./utils');

const getBrief = async (ws, reqId, { code }) => {
  let something = false;
  await Promise.allSettled([sources.indexav, sources.javlibrary, sources.javdb].map(
    (source) => source.getBrief(code).then((response) => {
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
  getBrief,
};
