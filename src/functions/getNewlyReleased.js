const sources = require('../sources');
const utils = require('./utils');

const getNewlyReleased = async (ws, reqId, { page }) => {
  await Promise.allSettled([sources.javlibrary, sources.javmost, sources.javdb].map(
    (source) => source.getNewlyReleased(page).then((response) => {
      if (response) {
        ws.send(JSON.stringify({ response, reqId }));
      }
    }).catch((err) => {
      utils.notFound(ws, reqId);
      throw err;
    }),
  ));
};

module.exports = {
  getNewlyReleased,
};
