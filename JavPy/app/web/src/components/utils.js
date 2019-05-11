import axios from "axios";
import config from "../config.js";
import Cookie from "js-cookie";

let set_userpass = (val) => {
    Cookie.set("userpass", val);
}

let get_userpass = () => {
    return Cookie.get("userpass");
}

let pookie = (url, data) => {
    let userpass = Cookie.get("userpass");
    if (userpass != null) {
        data.userpass = userpass;
    }
    return axios.post(`http://${config.address}:${config.port}${url}`, data);
}

let utils = {
    pookie,
    set_userpass,
    get_userpass
}

export default utils;