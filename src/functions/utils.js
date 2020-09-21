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

module.exports = {
  guessLang,
  notFound,
};
