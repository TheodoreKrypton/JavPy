const guessLang = (actress) => {
  for (let i = 0; i < actress.length; i += 1) {
    const charCode = actress.charCodeAt(i);
    if (charCode >= 128) {
      return 'jp';
    }
  }
  return 'en';
};

const notFound = (ws, reqId) => {
  ws.send(JSON.stringify({ response: 'not found', reqId }));
};

const expandSearch = {
  regexes: [
    {
      regex: new RegExp(/^\d+[-_]\d+$/),
      expander: (code) => [code.replace('-', '_'), code.replace('_', '-')],
    },
    {
      regex: new RegExp(/^RETOMN-\d+$/),
      expander: (code) => [code, code.slice(2, code.length)],
    },
    {
      regex: new RegExp(/\d+_ppv-.+/),
      expander: (code) => [code, code.replace(/\d+_ppv-/, '')],
    },
  ],

  getExpander(code) {
    for (let i = 0; i < this.regexes.length; i += 1) {
      if (code.match(this.regexes[i].regex)) {
        return this.regexes[i].expander;
      }
    }
    return null;
  },
};

module.exports = {
  guessLang,
  notFound,
  expandSearch,
};
