const express = require('express');
const fs = require('fs');
const sha256 = require('js-sha256');
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
  if (req.method !== 'POST' || req.originalUrl === '/auth_by_password') {
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

const FRONTEND_ROOT = path.join(argv.fe ? argv.fe : path.join(__dirname, '../../frontend/node_modules/javpy-react'), 'build/');

app.get('/', (req, res) => {
  fs.createReadStream(`${FRONTEND_ROOT}/index.html`)
    .pipe(res);
});

app.use(express.static(FRONTEND_ROOT));

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
  const ip = req.connection.remoteAddress;
  const { password } = req.body;
  if (!auth.checkIP(ip) || !auth.checkPassword(password)) {
    res.status(400);
    res.send('rejected');
    return;
  }

  const plain = [ip, password, new Date().time].join('/');
  const token = sha256.sha256(plain).slice(0, 24);
  auth.addToken(token);
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
