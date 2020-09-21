/* eslint-disable func-names */
/* eslint-disable prefer-arrow-callback */
/* eslint-disable no-undef */

const assert = require('assert');
const WS = require('./ws');
const functions = require('../src/functions');

describe('functions', function () {
  describe('search_by_code', function () {
    it('should not say not found', async function () {
      const ws = new WS();
      await functions.searchByCode(ws, '', { code: 'ABP-123' });
      assert.notEqual(ws.responses.length, 0);
      assert.notEqual(JSON.parse(ws.responses[0]).response, 'not found');
    });
  });
  describe('get_brief', function () {
    it('should not say not found', async function () {
      const ws = new WS();
      await functions.searchByCode(ws, '', { code: 'ABP-123' });
      assert.notEqual(ws.responses.length, 0);
      assert.notEqual(JSON.parse(ws.responses[0]).response, 'not found');
    });
  });
  describe('search_by_actress', function () {
    it('should have something', async function () {
      const ws = new WS();
      await functions.searchByActress(ws, '', { actress: 'Arina Hashimoto' });
      assert.notEqual(ws.responses.length, 0);
      let found = false;
      ws.responses.forEach((rsp) => {
        const obj = JSON.parse(rsp);
        if (obj.response !== 'not found' && obj.response.length > 0) {
          found = true;
        }
      });
      assert.equal(found, true);
    });
  });
  describe('search_magnet', function () {
    it('should not say not found', async function () {
      const ws = new WS();
      await functions.searchMagnet(ws, '', { code: 'ABP-123' });
      assert.notEqual(ws.responses.length, 0);
      assert.notEqual(JSON.parse(ws.responses[0]).response, 'not found');
    });
  });
  describe('get_aliases', function () {
    it('should have something', async function () {
      const ws = new WS();
      await functions.getAliases(ws, '', { actress: 'Eimi Fukada' });
      assert.notEqual(ws.responses.length, 0);
      assert.notEqual(JSON.parse(ws.responses[0]).response, 'not found');
    });
  });
  describe('get_newly_released', function () {
    it('should have something', async function () {
      const ws = new WS();
      await functions.getNewlyReleased(ws, '', { page: 1 });
      assert.notEqual(ws.responses.length, 0);
      let found = false;
      ws.responses.forEach((rsp) => {
        const obj = JSON.parse(rsp);
        if (obj.response !== 'not found' && obj.response.length > 0) {
          found = true;
        }
      });
      assert.equal(found, true);
    });
  });
});
