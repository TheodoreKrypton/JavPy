import React from 'react';
import utils from '../../utils';
import Videos from '../../components/Videos';
import api from '../../api';
import Alert from '@material-ui/lab/Alert';
import ActressProfile from '../../components/ActressProfile';
import Breadcrumbs from '@material-ui/core/Breadcrumbs';
import Button from '@material-ui/core/Button';
import { LinearProgress } from '@material-ui/core';

export default (props) => {
  const query = utils.useQuery();

  const [state, setState] = React.useState({
    historyNames: [],
    videos: [],
    actressProfile: null,
    loading: true,
    initialized: false
  })

  const unmounted = React.useRef(false);

  const handleClickHistoryName = (name) => {
    setState({
      ...state,
      videos: [],
      loading: true
    });
    api.searchByActress({ actress: name, withProfile: "false" }).then((rsp) => {
      setState({
        ...state,
        videos: rsp && rsp.videos.length ? rsp.videos : null,
        loading: false
      });
    })
  }

  const renderActressProfile = (actressProfile) => {
    if (!actressProfile) {
      return <></>
    }
    return <ActressProfile profile={actressProfile} name={query.get("actress")}></ActressProfile>
  }

  const renderHistoryNames = (historyNames) => {
    if (!historyNames) {
      return <></>
    } else {
      return (
        <div style={{
          display: "table",
          margin: "0 auto"
        }}>
          <Breadcrumbs aria-label="breadcrumb" >
            {historyNames.map((name, i) => {
              return <Button key={i.toString()} color="secondary" onClick={() => { handleClickHistoryName(name.trim()) }}> {name.trim()} </Button>
            })}
          </Breadcrumbs>
        </div>
      )
    }
  }

  const renderVideos = (videos) => {
    if (!videos || (!state.loading && videos.length === 0)) {
      return <Alert severity="error">Sorry. Cannot find the requested resources.</Alert>
    } else {
      return <Videos initialState={{ videosRendered: videos }}></Videos>
    }
  }

  const renderPage = ({ actressProfile, historyNames, videos, loading }) => {
    if (loading) {
      return <React.Fragment>
        <LinearProgress color="secondary"></LinearProgress>
        {renderActressProfile(actressProfile)}
        {renderHistoryNames(historyNames)}
      </React.Fragment>
    } else {
      return <React.Fragment>
        {renderActressProfile(actressProfile)}
        {renderHistoryNames(historyNames)}
        {renderVideos(videos)}
      </React.Fragment>
    }
  }

  React.useEffect(() => {
    if (!state.initialized) {
      api.searchByActress({ actress: query.get("actress"), withProfile: "true" }).then((rsp) => {
        if (unmounted.current) {
          return;
        }

        setState({
          ...state,
          ...rsp,
          loading: false,
          initialized: true
        })
      })
    } else {
      if (utils.globalCache.searchActress.recover === true) {
        utils.globalCache.searchActress.recover = false;
        window.scrollTo(0, utils.globalCache.searchActress.scrollY);
      }
    }

    window.onscroll = utils.debounce(() => {
      utils.globalCache.searchActress.scrollY = utils.getDocumentTop();
    }, 300)

    return () => {
      unmounted.current = true;
      window.onscroll = null;
    }
  })
  return renderPage(state)
}