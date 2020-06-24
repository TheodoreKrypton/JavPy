import React from 'react';
import Videos from '../../components/Videos';
import api from '../../api';
import utils from '../../utils';


export default (props) => {
  return (
    <Videos loadNextPage={api.getNewlyReleased} initialState={utils.globalCache.page.new}></Videos>
  )
}