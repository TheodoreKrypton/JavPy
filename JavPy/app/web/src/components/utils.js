import axios from "axios";
import config from "../config.js";
import Cookie from "js-cookie";

function setUserpass(val) {
    Cookie.set("userpass", val);
}

function getUserpass() {
    return Cookie.get("userpass");
}

async function pookie(url, data) {
    let userpass = Cookie.get("userpass");
    if (userpass != null) {
        if (data) {
            data.userpass = userpass;
        } else {
            data = {
                userpass: userpass
            }
        }
    }
    return await axios.post(`${config.address}:${config.port}${url}`, data).catch((err) => {
        if (err.response.status === 400) {
            Cookie.remove("userpass");
        }
    });
}

let globalCache = {
    searchActress: {}
}

let utils = {
    pookie,
    setUserpass,
    getUserpass,
    globalCache
}

export default utils;