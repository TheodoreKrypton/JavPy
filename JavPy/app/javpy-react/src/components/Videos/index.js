import React from 'react';
import useStyles from './styles';
import Box from '@material-ui/core/Box';
import VideoCard from './VideoCard';
import utils from '../../utils';


export default props => {
  const classes = useStyles();

  const { initialState, loadNextPage } = props;

  const [page, setPage] = React.useState(initialState.page);
  const [videosRendered, setVideosRendered] = React.useState(initialState.videosRendered);

  // const [loading, setLoading] = React.useState(false);

  const renderPage = () => {
    return (
      <React.Fragment>
        <Box
          className={classes.root}
          display="flex"
          flexWrap="wrap"
          justifyContent="center"
        >
          {videosRendered.map((video, i) => { return <VideoCard key={i.toString()} video={video} ></VideoCard> })}
        </Box>
      </React.Fragment>
    );
  }

  React.useEffect(() => {
    if (!window.onwheel) {
      window.onwheel = utils.debounce(() => {
        initialState.scrollY = utils.getDocumentTop();
        if (loadNextPage && utils.getScrollHeight() === utils.getWindowHeight() + utils.getDocumentTop()) {
          setPage(++initialState.page);
        }
      }, 100)
    }
  });

  React.useEffect(() => {
    if (initialState.scrollY) {
      window.scrollTo(0, initialState.scrollY);
    }

    return () => {
      window.onwheel = null;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  React.useEffect(() => {
    if (!loadNextPage) {
      return;
    }
    (async () => {
      const rsp = await loadNextPage({ page });
      if (rsp) {
        const videos = videosRendered.concat(rsp);
        initialState.videosRendered = videos;
        setVideosRendered(videos);
      }
    })()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page]);

  return renderPage();
}