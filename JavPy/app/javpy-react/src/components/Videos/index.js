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

  function renderPage({ videosRendered }) {
    return (<Box
      className={classes.root}
      display="flex"
      flexWrap="wrap"
      justifyContent="center"
    >
      {videosRendered.map((video, i) => { return <VideoCard key={i.toString()} video={video}></VideoCard> })}
    </Box>)
  }

  if (!loadNextPage) {
    return renderPage({ videosRendered: videos })
  }

  const [state, setState] = React.useState({
    page: 1,
    videosRendered: []
  })

  const unmounted = React.useRef(false);

  function loadMore() {
    loadNextPage({ page: state.page }).then((rsp) => {
      if (rsp && !unmounted.current) {
        setState({
          videosRendered: state.videosRendered.concat(rsp),
          page: state.page + 1
        });
      }
    })
  }

  React.useEffect(() => {
    window.onscroll = () => {
      unmounted.current = false;
      if (getScrollHeight() === getWindowHeight() + getDocumentTop()) {
        loadMore();
      }
    }
    if (state.videosRendered.length === 0) {
      loadMore();
    }

    return () => {
      unmounted.current = true;
      window.onscroll = null;
    }
  });

  return renderPage(state);
}