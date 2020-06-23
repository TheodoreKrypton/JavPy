import { useLocation } from "react-router-dom";

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

const globalCache = {
  new: {
    page: 1,
    videosRendered: []
  },
  searchActress: {
    videos: {},
    actressProfile: {},
    historyNames: {}
  },
  videos: {}
};

function getDocumentTop() {
  let scrollTop = 0,
    bodyScrollTop = 0,
    documentScrollTop = 0;

  if (document.body) {
    bodyScrollTop = document.body.scrollTop;
  }

  if (document.documentElement) {
    documentScrollTop = document.documentElement.scrollTop;
  }

  scrollTop =
    bodyScrollTop - documentScrollTop > 0
      ? bodyScrollTop
      : documentScrollTop;
  return scrollTop;
}

function getWindowHeight() {
  let windowHeight = 0;
  if (document.compatMode === "CSS1Compat") {
    windowHeight = document.documentElement.clientHeight;
  } else {
    windowHeight = document.body.clientHeight;
  }

  return windowHeight;
}

function getScrollHeight() {
  let scrollHeight = 0,
    bodyScrollHeight = 0,
    documentScrollHeight = 0;

  if (document.body) {
    bodyScrollHeight = document.body.scrollHeight;
  }

  if (document.documentElement) {
    documentScrollHeight = document.documentElement.scrollHeight;
  }
  scrollHeight =
    bodyScrollHeight - documentScrollHeight > 0
      ? bodyScrollHeight
      : documentScrollHeight;
  return scrollHeight;
}

const debounce = (func, delay) => {
  let inDebounce
  return function () {
    const context = this
    const args = arguments
    clearTimeout(inDebounce)
    inDebounce = setTimeout(() => func.apply(context, args), delay)
  }
}

export default { useQuery, globalCache, getDocumentTop, getScrollHeight, getWindowHeight, debounce };