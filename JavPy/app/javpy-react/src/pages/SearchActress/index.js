import React from 'react';
import utils from '../../utils';
import Videos from '../../components/Videos';
import api from '../../api';
import Alert from '@material-ui/lab/Alert';
import ActressProfile from '../../components/ActressProfile';
import Breadcrumbs from '@material-ui/core/Breadcrumbs';
import Button from '@material-ui/core/Button';
import { LinearProgress } from '@material-ui/core';

export default () => {
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
    setState(utils.assignState(state, { videos: [], loading: true }));
    api.searchByActress({ actress: name, withHistoryName: "false" }).then((rsp) => {
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
    return <ActressProfile info={actressProfile} name={query.get("actress")}></ActressProfile>
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
      return <Videos videos={videos}></Videos>
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
      Promise.all([
        api.searchByActress({ actress: query.get("actress"), withHistoryName: "true" }),
        api.actressInfo({ actress: query.get("actress") })
      ]).then((rsp) => {
        if (unmounted.current) {
          return;
        }
        let newState = {};
        if (rsp[0]) {
          newState.videos = rsp[0].videos;
          newState.historyNames = rsp[0].other.history_names;
        } else {
          newState.videos = null;
        }

        if (rsp[1]) {
          newState.actressProfile = rsp[1];
        }

        setState({
          ...state,
          ...newState,
          loading: false,
          initialized: true
        })
      })
    }
    return () => { unmounted.current = true }
  })
  return renderPage(state)

}