import React from 'react';
import Videos from '../../components/Videos';
import api from '../../api';
import utils from '../../utils';


export default (props) => {
  if (utils.globalCache.new.videos === null) {
    utils.globalCache.new.videos = [];
  }

  if (utils.globalCache.new.initialPage === null) {
    utils.globalCache.new.initialPage = 1;
  }

  const handleUpdate = (update) => {
    utils.globalCache.new = { ...utils.globalCache.new, ...update }
  }

  return (
    <Videos loadNextPage={api.getNewlyReleased} father="new" onUpdate={handleUpdate}></Videos>
  )
}