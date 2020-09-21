const { searchByActress } = require('./searchByActress');
const { getNewlyReleased } = require('./getNewlyReleased');
const { searchByCode } = require('./searchByCode');
const { searchMagnet } = require('./searchMagnet');
const { getActressProfile } = require('./getActressProfile');
const { getAliases } = require('./getAliases');
const { getBrief } = require('./getBrief');

module.exports = {
  searchByActress,
  getNewlyReleased,
  searchByCode,
  searchMagnet,
  getActressProfile,
  getAliases,
  getBrief,
};
