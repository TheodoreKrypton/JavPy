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

server.run(argv.port, openBrowser);
