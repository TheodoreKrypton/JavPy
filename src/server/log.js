const fs = require('fs');
const os = require('os');
const path = require('path');
const bunyan = require('bunyan-sfdx-no-dtrace');

const logPath = `${os.homedir()}${path.sep}.JavPy${path.sep}logs`;

if (!fs.existsSync(logPath)) {
  fs.mkdirSync(logPath, { recursive: true });
}

const logger = bunyan.createLogger({
  name: 'javpy',
  streams: [
    { stream: process.stdout },
    {
      type: 'rotating-file',
      path: `${logPath}${path.sep}javpy.log`,
      period: '1d',
      count: 30,
    },
  ],
});

module.exports = {
  logger,
};
