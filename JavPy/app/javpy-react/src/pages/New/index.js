import React from 'react';
import Videos from '../../components/Videos';
import api from '../../api';

export default (props) => {

  return (
    <Videos loadNextPage={api.getNewlyReleased}></Videos>
  )
}