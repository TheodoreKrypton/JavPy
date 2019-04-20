import axios from "axios";
import config from "../config.js";

let pookie = function (url, data) {
    return axios.post(`http://${config.address}:${config.port}${url}`, data, {
        withCredentials: true
    });
}

export default pookie;
