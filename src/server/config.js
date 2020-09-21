const fs = require('fs');
const os = require('os');
const path = require('path');
const packageJson = require('../../package.json');

const configDir = `${os.homedir()}${path.sep}.JavPy`;
const configPath = `${configDir}${path.sep}config.json`;

if (!fs.existsSync(configDir)) {
  fs.mkdirSync(configDir, { recursive: true });
}

if (!fs.existsSync(configPath)) {
  fs.writeFileSync(configPath, JSON.stringify({
    'ip-whitelist': ['127.0.0.1', '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16'],
    password: '',
    proxy: '',
    version: packageJson.version,
  }));
}

module.exports = {
  config: JSON.parse(fs.readFileSync(configPath)),
  set(newCfg) {
    fs.writeFileSync(configPath, JSON.stringify(newCfg));
    this.config = JSON.parse(fs.readFileSync(configPath));
  },
};
