import React from 'react';
import utils from '../../utils';
import Videos from '../../components/Videos';
import Async from 'react-async';
import api from '../../api';
import LinearProgress from '@material-ui/core/LinearProgress';
import Alert from '@material-ui/lab/Alert';
import ActressProfile from '../../components/ActressProfile';

export default () => {
  const query = utils.useQuery();


  return (
    <>
      <Async promiseFn={api.actressInfo} actress={query.get("actress")}>
        <Async.Pending>
          <LinearProgress color="secondary" />
        </Async.Pending>
        <Async.Fulfilled>
          {data => (
            <ActressProfile info={data} name={query.get("actress")}></ActressProfile>
          )}
        </Async.Fulfilled>
        <Async.Rejected>
          <></>
        </Async.Rejected>
      </Async>


      <Async promiseFn={api.searchByActress} actress={query.get("actress")} historyName={query.get("history_name")} >
        <Async.Pending>

        </Async.Pending>
        <Async.Fulfilled>
          {data => data.videos.length === 0 ? (<Alert severity="error">Sorry. Cannot find the requested resources.</Alert>) : (<Videos videos={data.videos}></Videos>)}
        </Async.Fulfilled>
        <Async.Rejected>
          {() => "Sorry. Nothing was found."}
        </Async.Rejected>
      </Async>
    </>
  )
}