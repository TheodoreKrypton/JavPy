import axios from 'axios';
import Cookie from "js-cookie";
import sha256 from 'js-sha256';
import utils from '../utils';


let address = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;

// only for developement
// address = `${window.location.protocol}//${window.location.hostname}:8081`;


function setUserpass(val) {
  Cookie.set("userpass", val);
}

function getUserpass() {
  return Cookie.get("userpass");
}

function hasUserpass() {
  return Cookie.get("userpass") !== undefined;
}

async function pookie(url, data) {
  const userpass = getUserpass();
  if (!userpass) {
    return
  }
  if (data) {
    data.userpass = userpass;
  } else {
    data = { userpass }
  }
  return await axios.post(`${address}${url}`, data).catch((err) => {
    if (!err.response || err.response.status === 400) {
      Cookie.remove("userpass");
      if (!utils.globalCache.refreshed) {
        utils.globalCache.refreshed = true;
        window.location.reload();
        utils.globalCache.refreshed = false;
      }
    }
  });
}

async function searchByCode({ code }) {
  if (utils.globalCache.videos[code] !== undefined) {
    return new Promise((resolve) => {
      resolve(utils.globalCache.videos[code]);
    })
  }

  const rsp = await pookie("/search_by_code", { code });
  if (rsp && rsp.status === 200 && rsp.data) {
    utils.globalCache.videos[code] = rsp.data.videos;
    return rsp.data.videos;
  } else {
    utils.globalCache.videos[code] = null;
    return null;
  }
}

async function getNewlyReleased({ page }) {
  const rsp = await pookie("/new", { page });
  if (rsp && rsp.status === 200 && rsp.data) {
    return rsp.data;
  } else {
    return null;
  }
}

async function searchByActress({ actress, withHistoryName }) {
  if (utils.globalCache.searchActress.videos[actress] !== undefined) {
    return new Promise((resolve) => {
      resolve({
        videos: utils.globalCache.searchActress.videos[actress],
        other: {
          history_name: utils.globalCache.searchActress.historyNames[actress]
        }
      });
    })
  }

  const rsp = await pookie("/search_by_actress", { actress, history_name: withHistoryName });
  if (rsp && rsp.status === 200 && rsp.data) {
    utils.globalCache.searchActress.videos[actress] = rsp.data.videos;

    const historyNames = rsp.data.other.history_names;
    if (historyNames) {
      utils.globalCache.searchActress.historyNames[actress] = historyNames;
      for (let i = 0; i < historyNames.length; i++) {
        utils.globalCache.searchActress.historyNames[historyNames[i]] = historyNames;
      }
    }

    return {
      videos: rsp.data.videos,
      other: rsp.data.other
    }
  } else {
    return null;
  }
}

async function actressInfo({ actress }) {
  if (utils.globalCache.searchActress.profile[actress] !== undefined) {
    return new Promise((resolve) => {
      resolve(utils.globalCache.searchActress.profile[actress]);
    })
  }

  const rsp = await pookie("/actress_info", { actress })
  if (rsp && rsp.status === 200 && rsp.data) {
    utils.globalCache.searchActress.profile[actress] = rsp.data;
    return rsp.data;
  } else {
    utils.globalCache.searchActress.profile[actress] = null;
    return null;
  }
}

async function searchMagnet({ code }) {
  const rsp = await pookie("/search_magnet_by_code", { code });
  if (rsp && rsp.status === 200 && rsp.data) {
    return rsp.data;
  } else {
    return null;
  }
}

async function authByPassword({ password }) {
  const rsp = await axios.post(`${address}/auth_by_password`, { password: sha256.sha256(password) });
  if (rsp && rsp.status === 200 && rsp.data) {
    setUserpass(rsp.data)
    return true;
  } else {
    return false;
  }
}

export default {
  address,
  hasUserpass,
  setUserpass,
  searchByCode,
  getNewlyReleased,
  searchByActress,
  actressInfo,
  searchMagnet,
  authByPassword
};