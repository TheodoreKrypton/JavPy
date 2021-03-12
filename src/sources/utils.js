const axios = require('axios');
const HttpsProxyAgent = require('https-proxy-agent');
const http = require('http');

const ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/85.0.4183.59 Chrome/85.0.4183.59 Safari/537.36';

module.exports = {
  requester: (baseUrl) => {
    let httpProxyConfig;
    let httpsProxyConfig;

    if (process.env.PROXY) {
      process.env.http_proxy = process.env.proxy;
      process.env.https_proxy = process.env.proxy;
    }

    if (process.env.http_proxy) {
      const [host, port] = process.env.http_proxy.split(':');
      httpProxyConfig = { host, port };
    }

    if (process.env.https_proxy) {
      const [host, port] = process.env.https_proxy.split(':');
      httpsProxyConfig = { host, port };
    }
    const requester = axios.create({
      timeout: 60000,
      httpAgent: new http.Agent({ keepAlive: true }),
      httpsAgent: new HttpsProxyAgent({ ...(httpsProxyConfig || {}), keepAlive: true }),
      proxy: httpProxyConfig,
    });

    const makeConfig = (config) => {
      if (!config) {
        return { headers: { 'User-Agent': ua } };
      }

      if (!config.headers) {
        return { headers: { 'User-Agent': ua }, ...config };
      }

      if (!config.headers['User-Agent']) {
        return { ...config, headers: { 'User-Agent': ua, ...config.headers } };
      }
      return config;
    };

    return {
      get(url, config) {
        const u = url.startsWith('http') ? url : `${baseUrl}${url}`;
        return requester.get(u, makeConfig(config))
          .catch((err) => console.error(`${baseUrl}${url} => ${err.message} `));
      },

      post(url, data, config) {
        const u = url.startsWith('http') ? url : `${baseUrl} ${url} `;
        console.log(data);
        return requester.post(u, data, makeConfig(config))
          .catch((err) => console.error(`${baseUrl}${url} => ${err.message} `));
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
      const rsp = await axios.head(url);
      return rsp.status >= 200 < 400;
    } catch {
      return false;
    }
  },
};
