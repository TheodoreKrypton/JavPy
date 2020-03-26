import React from 'react';
import Videos from '../../components/Videos';
import api from '../../api';
import Async from 'react-async';
import utils from "../../utils";
import LinearProgress from '@material-ui/core/LinearProgress';
import Alert from '@material-ui/lab/Alert';

export default () => {
  const query = utils.useQuery();

  return (
    <Async promiseFn={api.searchByCode} code={query.get("code")}>
      <Async.Pending>
        <LinearProgress color="secondary" />
      </Async.Pending>
      <Async.Fulfilled>
        {data => data === null ? (<Alert severity="error">Sorry. Cannot find the requested resources.</Alert>) : (<Videos videos={data}></Videos>)}
      </Async.Fulfilled>
      <Async.Rejected>
        {() => <Alert severity="error">Sorry. Cannot find the requested resources.</Alert>}
      </Async.Rejected>
    </Async>
  )
}