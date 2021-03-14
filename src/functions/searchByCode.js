const sources = require('../sources');
const utils = require('./utils');

const cartesian = (...a) => a.reduce((x, y) => x.flatMap((d) => y.map((e) => [d, e].flat())));

const searchByCode = async (ws, reqId, { code }) => {
  let something = false;

  let targets = [code];

  const expander = utils.expandSearch.getExpander(code);
  if (expander) {
    targets = expander(code);
  }

  await Promise.allSettled(
    cartesian([
      sources.javmost,
      sources.avgle,
      sources.youav,
      sources.highporn,
      sources.javhdporn,
      sources.javfull,
    ], targets)
      .map(([source, target]) => [[source, target.toUpperCase()], [source, target.toLowerCase()]])
      .reduce((input1, input2) => input1.concat(input2))
      .map(
        ([source, target]) => source.searchByCode(target).then(async (rsp) => {
          if (!rsp) {
            return;
          }
          if (Array.isArray(rsp)) {
            await Promise.allSettled(rsp.map((av) => av.then((response) => {
              if (response) {
                something = true;
                ws.send(JSON.stringify({ response, reqId }));
              }
            })));
          } else {
            something = true;
            ws.send(JSON.stringify({ response: rsp, reqId }));
          }
        }).catch((err) => {
          console.error(err.message);
        }),
      ),
  );
  if (!something) {
    utils.notFound(ws, reqId);
  }
};

module.exports = {
  searchByCode,
};
