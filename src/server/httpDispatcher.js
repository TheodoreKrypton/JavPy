const express = require('express');
const expressStaticGzip = require('express-static-gzip');
const cors = require('cors');
const path = require('path');
const yargs = require('yargs');
const auth = require('./authenticate');
const config = require('./config');
const { logger } = require('./log');

const { argv } = yargs
  .option('fe', {
    alias: 'f',
    description: 'frontend root',
    default: '',
    type: 'string',
  });

const app = express();

app.use(cors({ origin: true, credentials: true }));
app.use(express.json());

const beforeRequest = (req, res, next) => {
  logger.info({
    http: {
      ip: req.connection.remoteAddress,
      method: req.method,
      path: req.originalUrl,
      query: req.query,
      body: req.body,
    },
  });
  if (req.method !== 'POST' || req.originalUrl === '/auth_by_password' || req.originalUrl === '/is_public') {
    next();
    return;
  }
  const { userpass } = req.body;
  if (!auth.checkToken(userpass)) {
    res.status(400);
    res.send('rejected');
    return;
  }
  next();
};

app.use(beforeRequest);

const FRONTEND_ROOT = path.join(argv.fe ? argv.fe : path.join(__dirname, '../../frontend/'), 'build/');

app.use('/', expressStaticGzip(FRONTEND_ROOT));

// app.post('/', (req, res) => {
//   const { message } = req.body;
//   console.log('Regular POST message: ', message);
//   return res.json({
//     answer: 42,
//   });
// });

app.get('/redirect_to', (req, res) => {
  res.redirect(req.query.url);
});

app.post('/auth_by_password', (req, res) => {
  const ip = req.socket.remoteAddress;
  const { password } = req.body;

  const token = auth.authenticate(ip, password);

  if (token === null) {
    res.status(400);
    res.send('rejected');
    return;
  }

  res.send(token);
});

app.post('/is_public', (req, res) => {
  const ip = req.socket.remoteAddress;
  const token = auth.authenticate(ip, null);
  if (token === null) {
    res.status(400);
    res.send('rejected');
    return;
  }

  res.send(token);
});

app.post('/get_config', (req, res) => {
  const cfg = { ...config.config };
  cfg.password = '';
  res.send(JSON.stringify(cfg));
});

app.post('/update_config', (req, res) => {
  const cfg = { ...config.config };
  if (req.body.password !== '') {
    cfg['hashed-password'] = req.body.password;
  }
  cfg['ip-whitelist'] = req.body['ip-whitelist'];
  config.set(cfg);
  res.send('');
});

module.exports = app;
