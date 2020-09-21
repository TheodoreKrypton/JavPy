class WS {
  constructor() {
    this.responses = [];
  }

  send(msg) {
    this.responses.push(msg);
  }
}

module.exports = WS;
