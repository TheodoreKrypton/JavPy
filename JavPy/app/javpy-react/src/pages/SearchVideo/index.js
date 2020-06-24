import React from 'react';
import Videos from '../../components/Videos';
import api from '../../api';
import utils from "../../utils";
import LinearProgress from '@material-ui/core/LinearProgress';
import Alert from '@material-ui/lab/Alert';

export default () => {
  const query = utils.useQuery();
  const code = query.get("code");

  const [loading, setLoading] = React.useState(true);
  const [videos, setVideos] = React.useState([]);

  const render = () => {
    if (loading) {
      return <LinearProgress color="secondary" />
    } else {
      if (!videos) {
        return <Alert severity="error">Sorry. Cannot find the requested resources.</Alert>
      } else {
        return <Videos initialState={{ videosRendered: videos }}></Videos>
      }
    }
  }

  React.useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const rsp = await api.searchByCode({ code });
        if (rsp) {
          setVideos(rsp);
        }
      } finally {
        setLoading(false);
      }
    })()
  }, [code])

  return render();
}