import React from 'react';
import Videos from '../../components/Videos';
import api from '../../api';
import Async from 'react-async';
import LinearProgress from '@material-ui/core/LinearProgress';

export default (props) => {

  return (
    <Async promiseFn={api.getNewlyReleased} page={1}>
      <Async.Pending>
        <LinearProgress color="secondary" />
      </Async.Pending>
      <Async.Fulfilled>
        {data => (<Videos videos={data}></Videos>)}
      </Async.Fulfilled>
      <Async.Rejected>
        {() => "Sorry. All sources are down."}
      </Async.Rejected>
    </Async>
  )
}