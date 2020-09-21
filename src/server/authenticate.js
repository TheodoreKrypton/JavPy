const ipRangeCheck = require('ip-range-check');
const sha256 = require('js-sha256');
const config = require('./config');

const tokens = new Set();
let hashedPassword = '';
if (config.config['hashed-password']) {
  hashedPassword = config.config['hashed-password'];
} else {
  hashedPassword = sha256.sha256(config.config.password);
}

const addToken = (token) => {
  tokens.add(token);
};
const checkPassword = (password) => hashedPassword === password;
const checkIP = (ip) => ipRangeCheck(ip, config.config['ip-whitelist']);
const checkToken = (token) => tokens.has(token);

module.exports = {
  checkPassword,
  checkToken,
  checkIP,
  addToken,
};
