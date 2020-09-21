const sources = require('../sources');
const utils = require('./utils');

const getActressProfile = async (ws, reqId, { actress }) => {
  try {
    const rsp = sources.warashiAsianPornstarsFr.getActressProfile(actress);
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
  getActressProfile,
};
