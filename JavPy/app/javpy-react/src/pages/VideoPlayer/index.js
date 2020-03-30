import "video-react/dist/video-react.css"; // import css
import React from 'react';
import { Player } from 'video-react';
import utils from '../../utils';
import HLSSource from './HlsSource';

export default props => {
  const video_url = utils.useQuery().get("video_url");
  if (video_url.endsWith(".m3u8")) {
    return (
      <Player playsInline>
        <HLSSource
          isVideoChild
          src={decodeURIComponent(video_url)}
        />
      </Player>
    );
  } else {
    return (
      <Player
        playsInline
        src={decodeURIComponent(video_url)}>
      </Player>
    )
  }
};