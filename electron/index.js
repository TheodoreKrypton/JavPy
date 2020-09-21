/* eslint-disable import/no-extraneous-dependencies */
const { app, BrowserWindow } = require('electron');
const server = require('../src/server');

const PORT = 8081;

function createWindow() {
  // Create the browser window.
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
    },
  });
  win.setMenu(null);
  // and load the index.html of the app.
  win.loadURL(`http://localhost:${PORT}`);
}

app.whenReady().then(() => {
  server.run(8081, createWindow);
});
