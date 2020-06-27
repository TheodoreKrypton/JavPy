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

  const [historyNames, setHistoryNames] = React.useState([]);
  const [videos, setVideos] = React.useState([]);
  const [actressProfile, setActressProfile] = React.useState(null);
  const [loading, setLoading] = React.useState(true);

  const handleClickHistoryName = (name) => {
    setVideos([]);
    setLoading(true);
    api.searchByActress({ actress: name, withProfile: "false" }).then((rsp) => {
      if (rsp) {
        setVideos(rsp.data);
      }
    }).finally(() => {
      setLoading(false);
    })
  }

  const renderActressProfile = () => {
    return <ActressProfile profile={actressProfile} name={query.get("actress")}></ActressProfile>
  }

  const renderHistoryNames = () => {
    return (
      <div style={{
        display: "table",
        margin: "0 auto"
      }}>
        <Breadcrumbs>
          {historyNames.map((name, i) => {
            return <Button key={i.toString()} color="secondary" onClick={() => { handleClickHistoryName(name.trim()) }}> {name.trim()} </Button>
          })}
        </Breadcrumbs>
      </div>
    )
  }

  const VIDEOS_PER_PAGE = 16;

  const loadNextPage = ({ page }) => {
    return videos.slice((page - 1) * VIDEOS_PER_PAGE, page * VIDEOS_PER_PAGE);
  }

  const renderVideos = () => {
    console.log(loading, videos);
    if (loading) {
      return <></>
    } else if (!videos || videos.length === 0) {
      return <Alert severity="error">Sorry. Cannot find the requested resources.</Alert>
    } else {
      return <Videos initialState={utils.globalCache.page.searchActress} loadNextPage={loadNextPage}></Videos>
    }
  }

  React.useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const rsp = await api.searchByActress({ actress: query.get("actress"), withProfile: "true" });
        if (rsp) {
          setVideos(rsp.videos);
          setHistoryNames(rsp.historyNames);
          setActressProfile(rsp.actressProfile);
        }
      } finally {
        setLoading(false);
      }
    })()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <React.Fragment>
      {loading ? <LinearProgress color="secondary"></LinearProgress> : <></>}
      {actressProfile ? renderActressProfile() : <></>}
      {historyNames ? renderHistoryNames() : <></>}
      {renderVideos()}
    </React.Fragment>
  )
}