const functions = require('../functions');
const auth = require('./authenticate');
const { logger } = require('./log');

const dispatch = (ws, msg) => {
  logger.info({ ws: msg });

  try {
    const { message, reqId, userpass } = msg;

    if (!auth.checkToken(userpass)) {
      return;
    }

    const { api, args } = message;

    const routes = {
      search_by_code: functions.searchByCode,
      get_newly_released: functions.getNewlyReleased,
      search_by_actress: functions.searchByActress,
      search_magnet_by_code: functions.searchMagnet,
      get_aliases: functions.getAliases,
      get_actress_profile: functions.getActressProfile,
      get_brief: functions.getBrief,
    };

    if (routes[api]) {
      routes[api](ws, reqId, args);
    }
  } catch (err) {
    logger.error(err.message);
  }
};

module.exports = {
  dispatch,
};
