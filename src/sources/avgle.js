const Axios = require('axios').default;
const utils = require('./utils');
const ds = require('../ds');

const requester = utils.requester('https://api.avgle.com');

const searchByCode = async (code) => {
  const rsp = await requester.get(`/v1/search/${code}/0?limit=1`);
  const video = rsp.data.response.videos[0];

  const testVideo = await Axios.get(encodeURI(video.video_url), { maxRedirects: 0 });
  if (testVideo.status === 301) {
    return null;
  }

  if (video.title.toLowerCase().includes(code.toLowerCase())) {
    const av = new ds.AV();
    av.title = video.title;
    av.video_url = video.video_url;
    av.code = code;
    av.preview_img_url = video.preview_url;
    return av;
  }
  return null;
};

module.exports = {
  searchByCode,
};
