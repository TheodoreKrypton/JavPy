const sources = require('../sources');
const utils = require('./utils');

const getAliases = async (ws, reqId, { actress }) => {
  try {
    const rsp = await sources.warashiAsianPornstarsFr.getAliases(actress);
    if (rsp) {
      ws.send(JSON.stringify({ response: rsp, reqId }));
    } else {
      utils.notFound(ws, reqId);
    }
  } catch (err) {
    utils.notFound(ws, reqId);
  }
};

module.exports = {
  getAliases,
};
