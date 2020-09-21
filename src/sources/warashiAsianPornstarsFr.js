const { JSDOM } = require('jsdom');
const utils = require('./utils');
const ds = require('../ds');
const { noexcept } = require('./utils');

const requester = utils.requester('http://warashi-asian-pornstars.fr');
const cached = {
  actressDetailUrl: {},
  alias: {},
  actressInfo: {},
};

const getNameInCard = (name, card) => {
  if (!card) {
    return null;
  }

  if (!card.textContent.toLowerCase().includes(name)) {
    return null;
  }

  const title = card.querySelector('p').textContent.toLowerCase();

  const jpName = title.split('-')[1].trim();
  if (jpName.length === 0) {
    return null;
  }

  // cache for parsing actress info later, None for no url
  const url = noexcept(() => card.querySelector('a').href);
  cached.actressDetailUrl[name] = url;
  cached.actressDetailUrl[jpName] = url;

  return jpName;
};

const translate2Jp = async (actress) => {
  const payload = `recherche_critere=f&recherche_valeur=${encodeURIComponent(actress)}`;

  const rsp = await requester.post('/en/s-12/search', payload, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  const dom = new JSDOM(rsp.data).window.document;
  const actressLower = actress.toLowerCase();

  const name = getNameInCard(actressLower, dom.querySelector('.resultat-pornostar'))
    || getNameInCard(actressLower, utils.noexcept(() => dom.querySelector('#bloc-resultats-conteneur-pornostars').querySelector('.resultat-pornostar')))
    || getNameInCard(actressLower, utils.noexcept(() => dom.querySelector('#bloc-resultats-conteneur-castings').querySelector('.resultat-pornostar')));

  if (name) return name;

  cached.actressDetailUrl[name] = null;
  return null;
};

const getBriefFromTr = (tr) => {
  const av = new ds.AV();
  av.preview_img_url = noexcept(() => tr.getAttribute('data-img'));
  if (av.preview_img_url && av.preview_img_url.startsWith('/')) {
    av.preview_img_url = `http://warashi-asian-pornstars.fr${av.preview_img_url}`.replace('/mini/', '/large/');
  }
  const tds = [...tr.querySelectorAll('td')];
  av.title = tds[1].textContent.trim();
  av.code = tds[2].textContent.toUpperCase();
  av.release_date = tds[5].textContent.trim();
  return av;
};

const searchByActress = async (actress) => {
  const actressLower = actress.toLowerCase();
  if (cached.actressDetailUrl[actressLower] === undefined) {
    await translate2Jp(actress);
  }
  if (!cached.actressDetailUrl[actressLower]) {
    return [];
  }
  const rsp = await requester.get(cached.actressDetailUrl[actressLower].replace('/s-2-0/', '/s-2-4/'));
  const dom = new JSDOM(rsp.data).window.document;
  const trs = [...dom.querySelector('table').querySelectorAll('tr')];
  const res = trs.slice(1, trs.length).map(getBriefFromTr);
  return res;
};

const parseDetailPage = async (actress) => {
  const actressLower = actress.toLowerCase();
  if (cached.actressInfo[actressLower] !== undefined && cached.alias[actressLower] !== undefined) {
    return;
  }

  if (cached.actressDetailUrl[actressLower] === undefined) {
    await translate2Jp(actress);
  }
  const url = cached.actressDetailUrl[actressLower];
  if (!url) {
    return;
  }
  const rsp = await requester.get(url);
  const dom = new JSDOM(rsp.data).window.document;

  const actressInfo = new ds.Actress();
  const img = dom.querySelector('#pornostar-profil-photos') || dom.querySelector('#casting-profil-preview');
  if (img) {
    actressInfo.img = `http://warashi-asian-pornstars.fr/${img.querySelector('img').src}`;
  }

  const infoField = dom.querySelector('#pornostar-profil-infos');

  if (!infoField) {
    cached.actressInfo[actressLower] = null;
    cached.alias[actressLower] = null;
    cached.actressInfo[actressLower] = actressInfo;
    return;
  }

  if (cached.actressInfo[actressLower] === undefined) {
    const ps = infoField.querySelectorAll('p');
    ps.forEach((p) => {
      try {
        if (p.textContent.includes('birthdate')) {
          actressInfo.birth_date = p.querySelector('time').getAttribute('content');
        }
        if (p.getAttribute('itemprop')) {
          if (p.getAttribute('itemprop') === 'height') {
            actressInfo.height = p.querySelector('span').textContent.trim();
          } else if (p.getAttribute('itemprop') === 'weight') {
            actressInfo.weight = p.querySelector('span').textContent.trim();
          }
        }
        // eslint-disable-next-line no-empty
      } catch { }
    });

    cached.actressInfo[actressLower] = actressInfo;
  }

  if (cached.alias[actressLower] === undefined) {
    const aliases = new Set();
    const h1 = dom.querySelector('h1');
    const mainName = h1.querySelectorAll('span')[1].textContent;
    aliases.add(mainName);

    const div = infoField.querySelector('#pornostar-profil-noms-alternatifs');
    if (div) {
      const names = [...div.querySelectorAll('li')].map((li) => {
        const spans = li.querySelectorAll('span');
        if (spans.length === 0) {
          return null;
        }
        return spans[1].textContent.trim();
      }).filter((x) => x !== null);
      names.forEach((name) => {
        aliases.add(name);
      });

      aliases.forEach((alias) => {
        cached.alias[alias.toLowerCase()] = aliases;
        cached.actressInfo[alias.toLowerCase()] = cached.actressInfo[actressLower];
      });
    } else {
      cached.alias[actressLower] = null;
    }

    cached.alias[actressLower] = aliases;
  }
};

const getActressProfile = async (actress) => {
  await parseDetailPage(actress);
  return cached.actressInfo[actress.toLowerCase()];
};

const getAliases = async (actress) => {
  await parseDetailPage(actress);
  if (cached.alias[actress.toLowerCase()]) {
    return [...cached.alias[actress.toLowerCase()]];
  }
  return null;
};

module.exports = {
  searchByActress,
  translate2Jp,
  getActressProfile,
  getAliases,
};
