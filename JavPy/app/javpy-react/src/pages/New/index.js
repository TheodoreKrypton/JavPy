import React from 'react';
import Videos from '../../components/Videos';
import api from '../../api';
import Async from 'react-async';
import LinearProgress from '@material-ui/core/LinearProgress';

export default (props) => {
  const [page] = React.useState(1);

  return (

    <Async promiseFn={api.getNewlyReleased} page={page}>
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