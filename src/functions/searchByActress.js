const sources = require('../sources');
const utils = require('./utils');

const searchByActress = async (ws, reqId, { actress }) => {
  const lang = utils.guessLang(actress);
  if (lang === 'en') {
    try {
      // eslint-disable-next-line no-param-reassign
      actress = await sources.warashiAsianPornstarsFr.translate2Jp(actress);
    } catch (err) {
      console.error(err);
    }
    if (!actress) {
      utils.notFound(ws, reqId);
    }
  }

  let something = false;
  await Promise.allSettled([
    sources.indexav,
    sources.warashiAsianPornstarsFr,
  ].map((source) => source.searchByActress(actress).then(async (rsp) => {
    if (!rsp) {
      return;
    }
    if (rsp.length > 0 && rsp[0] instanceof Promise) {
      await Promise.allSettled(rsp.map((r) => r.then((response) => {
        if (response) {
          something = true;
          ws.send(JSON.stringify({ response, reqId }));
        }
      })));
    } else {
      something = true;
      ws.send(JSON.stringify({ response: rsp, reqId }));
    }
  })));
  if (!something) {
    utils.notFound(ws, reqId);
  }
};

module.exports = {
  searchByActress,
};
