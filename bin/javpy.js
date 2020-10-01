#!/usr/bin/env node

const yargs = require('yargs');
const { exec } = require('child_process');
const os = require('os');
const server = require('../src/server');

const { argv } = yargs
  .option('port', {
    alias: 'p',
    description: 'listen to port',
    default: 8081,
    type: 'int',
  })
  .option('browser', {
    description: 'open browser automatically',
    default: true,
    type: 'bool',
  })
  .help()
  .alias('help', 'h');

const openBrowser = () => {
  const url = `http://localhost:${argv.port}`;
  const platform = os.platform();
  if (platform.includes('win32')) {
    exec(`start "" "${url}"`);
  } else if (platform.includes('linux')) {
    exec(`xdg-open ${url}`);
  } else {
    exec(`open ${url}`);
  }
};

server.run(argv.port, argv.browser === 'false' ? undefined : openBrowser);
