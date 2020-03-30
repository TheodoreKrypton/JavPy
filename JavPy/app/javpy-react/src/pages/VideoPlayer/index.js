import "video-react/dist/video-react.css"; // import css
import React from 'react';
import { Player } from 'video-react';
import utils from '../../utils';
import HLSSource from './HlsSource';

export default props => {
  return (
    <Player playsInline>
      <HLSSource
        isVideoChild
        src={decodeURIComponent(utils.useQuery().get("video_url"))}
      />
    </Player>
  );
};