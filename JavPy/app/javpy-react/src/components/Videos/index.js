import React from 'react';
import useStyles from './styles';
import Box from '@material-ui/core/Box';
import VideoCard from './VideoCard';
import utils from '../../utils';


export default props => {
  const classes = useStyles();

  const { videos, loadNextPage, onUpdate, father } = props;
  const fatherCache = father ? utils.globalCache[father] : undefined;

  function renderPage({ videosRendered }) {
    return (
      <React.Fragment>
        <Box
          className={classes.root}
          display="flex"
          flexWrap="wrap"
          justifyContent="center"
        >
          {videosRendered.map((video, i) => { return <VideoCard key={i.toString()} video={video}></VideoCard> })}
        </Box>
      </React.Fragment>
    )
  }

  if (!loadNextPage) {
    return renderPage({ videosRendered: videos })
  }

  const [state, setState] = React.useState(fatherCache ? {
    page: fatherCache.initialPage,
    videosRendered: fatherCache.videos,
  } : {
      page: 1,
      videosRendered: [],
    })

  const unmounted = React.useRef(false);

  function update(things) {
    if (onUpdate) {
      onUpdate(things)
    }
  }

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
    update({
      videos: state.videosRendered,
      initialPage: state.page
    })
    if (fatherCache.recover) {
      window.scrollTo(0, fatherCache.scrollY);
      fatherCache.recover = false;
    }

    window.onscroll = utils.debounce(() => {
      update({ scrollY: utils.getDocumentTop() })
      unmounted.current = false;
      if (utils.getScrollHeight() === utils.getWindowHeight() + utils.getDocumentTop()) {
        loadMore();
      }
    }, 300);

    if (state.videosRendered.length === 0) {
      loadMore();
    }

    return () => {
      unmounted.current = true;
      window.onscroll = null;
    }
  });

  if (!state.initialized) {
    setState({ ...state, initialized: true })
  }

  return renderPage(state);
}