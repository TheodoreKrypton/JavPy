import axios from "axios";
import config from "../config.js";
import Cookie from "js-cookie";

let set_userpass = (val) => {
    Cookie.set("userpass", val);
}

let get_userpass = () => {
    return Cookie.get("userpass");
}

let pookie = async (url, data) => {
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
    return await axios.post(`http://${config.address}:${config.port}${url}`, data).catch((err) => {
        if (err.response.status === 400) {
            Cookie.remove("userpass");
        }
    });
}

let utils = {
    pookie,
    set_userpass,
    get_userpass
}

export default utils;