/* eslint-disable func-names */
/* eslint-disable prefer-arrow-callback */
/* eslint-disable no-undef */

const assert = require('assert');
const { default: axios } = require('axios');
const WS = require('./ws');
const functions = require('../src/functions');

describe('functions', function () {
  describe('search_by_code', function () {
    it('should not say not found', async function () {
      const ws = new WS();
      await functions.searchByCode(ws, '', { code: 'ABP-123' });
      assert.notStrictEqual(ws.responses.length, 0);
      assert.notStrictEqual(JSON.parse(ws.responses[0]).response, 'not found');
    });
  });
  describe('get_brief', function () {
    it('should not say not found', async function () {
      const ws = new WS();
      await functions.getBrief(ws, '', { code: 'ABP-123' });
      assert.notStrictEqual(ws.responses.length, 0);
      assert.notStrictEqual(JSON.parse(ws.responses[0]).response, 'not found');
    });
  });
  describe('search_by_actress', function () {
    it('should have something', async function () {
      const ws = new WS();
      await functions.searchByActress(ws, '', { actress: 'Arina Hashimoto' });
      assert.notStrictEqual(ws.responses.length, 0);
      let found = false;
      ws.responses.forEach((rsp) => {
        const obj = JSON.parse(rsp);
        if (obj.response !== 'not found' && obj.response.length > 0) {
          found = true;
        }
      });
      assert.strictEqual(found, true);
    });
  });
  describe('search_magnet', function () {
    it('should not say not found', async function () {
      const ws = new WS();
      await functions.searchMagnet(ws, '', { code: 'ABP-123' });
      assert.notStrictEqual(ws.responses.length, 0);
      assert.notStrictEqual(JSON.parse(ws.responses[0]).response, 'not found');
    });
  });
  describe('get_aliases', function () {
    it('should have something', async function () {
      const ws = new WS();
      await functions.getAliases(ws, '', { actress: 'Eimi Fukada' });
      assert.notStrictEqual(ws.responses.length, 0);
      assert.notStrictEqual(JSON.parse(ws.responses[0]).response, 'not found');
    });
  });

  describe('get_actress_profile', function () {
    it('should have something', async function () {
      const ws = new WS();
      await functions.getActressProfile(ws, '', { actress: '深田えいみ' });
      assert.notStrictEqual(ws.responses.length, 0);
      assert.notStrictEqual(JSON.parse(ws.responses[0]).response, 'not found');
    });
  });

  describe('get_newly_released', function () {
    it('should have something', async function () {
      const ws = new WS();
      await functions.getNewlyReleased(ws, '', { page: 1 });
      assert.notStrictEqual(ws.responses.length, 0);
      let found = false;
      ws.responses.forEach((rsp) => {
        const obj = JSON.parse(rsp);
        if (obj.response !== 'not found' && obj.response.length > 0) {
          found = true;
        }
      });
      assert.strictEqual(found, true);
    });
  });

  describe('search_actress_by_image', function () {
    it('should have something', async function () {
      const ws = new WS();
      const rsp = await axios.get('https://i.imgur.com/t0JcBh1.jpg', { responseType: 'arraybuffer' });
      const dataUrl = `data:image/jpeg;base64,${Buffer.from(rsp.data).toString('base64')}`;
      await functions.searchActressByImage(ws, '', { image: dataUrl });
      assert.notStrictEqual(ws.responses.length, 0);
    });
  });
});
