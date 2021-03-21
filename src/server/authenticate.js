const ipRangeCheck = require('ip-range-check');
const sha256 = require('js-sha256');
const config = require('./config');

const [isPublic, setPublic] = (() => {
  let publicMode = false;
  return [() => publicMode, () => { publicMode = true; }];
})();

const [hasToken, addToken] = (() => {
  const tokens = new Set();
  return [(token) => tokens.has(token), (token) => tokens.add(token)];
})();

const hashedPassword = (() => {
  if (config.config['hashed-password']) {
    return config.config['hashed-password'];
  }
  return sha256.sha256(config.config.password);
})();

const genToken = (ip, password) => sha256.sha256(`${ip}/${password}/${new Date().time}`).slice(0, 24);
const checkPassword = (password) => hashedPassword === password;
const checkIP = (ip) => isPublic() || ipRangeCheck(ip, config.config['ip-whitelist']);
const checkToken = (token) => isPublic() || hasToken(token);

const authenticate = (ip, password) => {
  if ((isPublic() && password === null) || (checkIP(ip) && checkPassword(password))) {
    const token = genToken(ip, password);
    addToken(token);
    return token;
  }
  return null;
};

module.exports = {
  authenticate,
  checkToken,
  setPublic,
};
