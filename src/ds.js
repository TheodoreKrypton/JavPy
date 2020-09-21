/* eslint-disable max-classes-per-file */
class AV {
  constructor() {
    this.code = null;
    this.title = null;
    this.video_url = null;
    this.preview_img_url = null;
    this.actress = [];
    this.release_date = null;
  }
}

class Magnet {
  constructor() {
    this.magnet = null;
    this.description = null;
    this.peers = null;
  }
}

class Actress {
  constructor() {
    this.birth_date = null;
    this.img = null;
    this.height = null;
    this.weight = null;
  }
}

module.exports = {
  AV, Magnet, Actress,
};
