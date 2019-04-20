import axios from "axios";
import config from "../config.js";

let post_with_cookie = function (url, data) {
    return axios.post(`http://${config.address}:${config.port}${url}`, data, {
        withCredentials: true
    });
}

export default post_with_cookie;
