// eslint-disable-file

const WebSocket = require('ws');
const server = require('http').createServer();
const wsDispatcher = require('./wsDispatcher');
const httpDispatcher = require('./httpDispatcher');

const wss = new WebSocket.Server({ path: '/ws/', server });
server.on('request', httpDispatcher);

wss.on('connection', (ws) => {
  console.log('connected');
  ws.on('message', (message) => {
    wsDispatcher.dispatch(ws, JSON.parse(message));
  });
});

function noop() { }

const interval = setInterval(() => {
  wss.clients.forEach((ws) => {
    if (ws.isAlive === false) return ws.terminate();

    // eslint-disable-next-line no-param-reassign
    ws.isAlive = false;
    ws.ping(noop);
  });
}, 60 * 60 * 1000);

wss.on('close', () => {
  clearInterval(interval);
});

const run = (port, cb) => {
  console.log(
    '       __            ____       \n'
    + '      / /___ __   __/ __ \\__  __\n'
    + ' __  / / __ `/ | / / /_/ / / / /\n'
    + '/ /_/ / /_/ /| |/ / ____/ /_/ / \n'
    + '\\____/\\__,_/ |___/_/    \\__, /  \n'
    + '                       /____/   \n',
  );
  server.listen(port, '0.0.0.0', () => {
    console.log(`server listening on ${port} `);
    if (cb) {
      cb();
    }
  });
};

module.exports = {
  run,
};
