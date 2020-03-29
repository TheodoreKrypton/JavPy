import axios from 'axios';
import Cookie from "js-cookie";


let address = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;

// only for developement
address = `${window.location.protocol}//${window.location.hostname}:8081`;


function setUserpass(val) {
  Cookie.set("userpass", val);
}

function getUserpass() {
  return Cookie.get("userpass");
}

async function pookie(url, data) {
  const userpass = getUserpass();
  if (userpass != null) {
    if (data) {
      data.userpass = userpass;
    } else {
      data = { userpass }
    }
  }
  return await axios.post(`${address}${url}`, data).catch((err) => {
    if (err.response.status === 400) {
      Cookie.remove("userpass");
    }
  });
}

async function searchByCode({ code }) {
  const rsp = await pookie("/search_by_code", { code });
  if (rsp.status === 200 && rsp.data) {
    return rsp.data.videos;
  } else {
    return null;
  }
}

async function getNewlyReleased({ page }) {
  const rsp = await pookie("/new", { page });
  if (rsp.status === 200 && rsp.data) {
    return rsp.data;
  } else {
    return null;
  }
}

async function searchByActress({ actress, withHistoryName }) {
  const rsp = await pookie("/search_by_actress", { actress, history_name: withHistoryName });
  if (rsp.status === 200 && rsp.data) {
    return {
      videos: rsp.data.videos,
      other: rsp.data.other
    }
  } else {
    return null;
  }
}

async function actressInfo({ actress }) {
  const rsp = await pookie("/actress_info", { actress })
  if (rsp.status === 200 && rsp.data) {
    return rsp.data;
  } else {
    return null;
  }
}

async function searchMagnet({ code }) {
  const rsp = await pookie("/search_magnet_by_code", { code });
  if (rsp.status === 200 && rsp.data) {
    return rsp.data;
  } else {
    return null;
  }
}

export default {
  address,
  setUserpass,
  searchByCode,
  getNewlyReleased,
  searchByActress,
  actressInfo,
  searchMagnet
};