import Event from "../main";

function search(video) {
  if (video.actress) {
    Event.$emit("search_by_actress", {
      actress: video.actress
    });
  } else if (video.code) {
    Event.$emit("search_by_code", {
      code: video.code
    });
  }
}

function magnet(video) {
  Event.$emit("search_magnet_by_code", video);
}

let guider = {
  search,
  magnet
}

export default guider;