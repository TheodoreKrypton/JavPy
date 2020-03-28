import React from 'react';
import useStyles from './styles';
import Box from '@material-ui/core/Box';
import VideoCard from './VideoCard';

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

export default props => {
  const classes = useStyles();

  const { videos, loadNextPage } = props;

  const renderPage = (videosToRender) => {
    return <Box
      className={classes.root}
      display="flex"
      flexWrap="wrap"
      justifyContent="center"
    >
      {videosToRender.map((video, i) => { return <VideoCard key={i.toString()} video={video}></VideoCard> })}
    </Box>

  }

  if (videos) {
    return renderPage(videos)
  }

  const loadVideos = (() => {
    let page = 0;
    return async () => {
      page++;
      return await loadNextPage(page);
    }
  })();

  const [videosRendered, setVideosRendered] = React.useState([]);

  window.onscroll = () => {
    if (getScrollHeight() === getWindowHeight() + getDocumentTop()) {
      loadVideos().then((rsp) => {
        setVideosRendered(videosRendered.concat(rsp));
      })
    }
  };

  if (videosRendered.length === 0) {
    loadVideos().then((rsp) => {
      setVideosRendered(rsp);
    })
  }

  return renderPage(videosRendered);
}