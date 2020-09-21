const axios = require('axios');
const http = require('http');
const https = require('https');
const { default: Axios } = require('axios');
const { JSDOM } = require('jsdom');

let ua = null;

const getUserAgent = async () => {
  if (!ua) {
    const rsp = await Axios.get('https://user-agents.net/browsers/chromium');
    const dom = new JSDOM(rsp.data).window.document;
    ua = dom.querySelector('.agents_list').querySelector('li').textContent;
  }
  return ua;
};

module.exports = {
  requester: (baseUrl) => {
    const requester = axios.create({
      timeout: 60000,
      httpAgent: new http.Agent({ keepAlive: true }),
      httpsAgent: new https.Agent({ keepAlive: true }),
    });

    const makeConfig = (config) => {
      if (!config) {
        return { headers: { 'User-Agent': getUserAgent() } };
      }

      if (!config.headers) {
        return { headers: { 'User-Agent': getUserAgent() }, ...config };
      }

      if (!config.headers['User-Agent']) {
        return { ...config, headers: { 'User-Agent': getUserAgent(), ...config.headers } };
      }
      return config;
    };

    return {
      get(url, config) {
        const u = url.startsWith('http') ? url : `${baseUrl}${url}`;
        return requester.get(u, makeConfig(config))
          .catch((err) => console.error(`${baseUrl} => ${err.message}`));
      },

      post(url, data, config) {
        const u = url.startsWith('http') ? url : `${baseUrl}${url}`;
        return requester.post(u, data, makeConfig(config))
          .catch((err) => console.error(`${baseUrl} => ${err.message}`));
      },
    };
  },

  noexcept: (lambdaFn) => {
    try {
      return lambdaFn();
    } catch (err) {
      return null;
    }
  },

  testUrl: async (url) => {
    try {
      const rsp = await Axios.head(url);
      return rsp.status >= 200 < 400;
    } catch {
      return false;
    }
  },
};
