import React from 'react';
import useStyles from './styles';
import Box from '@material-ui/core/Box';
import VideoCard from './VideoCard';


export default props => {
  const classes = useStyles();

  return (
    <Box
      className={classes.root}
      display="flex"
      flexWrap="wrap"
      justifyContent="center"
    >
      {props.videos.map((video, i) =>
        <VideoCard key={i.toString()} video={video}></VideoCard>
      )}
    </Box>
  )
}