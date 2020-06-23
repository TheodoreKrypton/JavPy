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
  const [initialized, setInitialized] = React.useState(false);

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

  if (!loadNextPage) {
    return renderPage();
  }

  React.useEffect(() => {
    (async () => {
      if (!initialized) {
        window.onscroll = utils.debounce(() => {
          initialState.scrollY = utils.getDocumentTop();
          if (utils.getScrollHeight() === utils.getWindowHeight() + utils.getDocumentTop()) {
            initialState.page = page + 1;
            setPage(initialState.page);
          }
        }, 100);

        if (initialState.scrollY) {
          window.scrollTo(0, initialState.scrollY);
        }

        setInitialized(true);
      }
      const rsp = await loadNextPage({ page });
      if (rsp) {
        initialState.videosRendered = videosRendered.concat(rsp);
        setVideosRendered(initialState.videosRendered);
      }
    })()
    return () => {
      delete window.onscroll;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page]);

  return renderPage();
}