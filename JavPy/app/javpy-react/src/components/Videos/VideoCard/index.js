import React from 'react';
import useStyles from './styles'
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import { useHistory } from 'react-router-dom';
import LazyLoad from 'react-lazyload';
import Chip from '@material-ui/core/Chip';
import api from '../../../api';

export default props => {
  const classes = useStyles();
  const history = useHistory();
  const { video } = props;

  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMultipleClick = event => {
    setAnchorEl(event.currentTarget);
  };

  const handleMultipleClose = () => {
    setAnchorEl(null);
  };

  const handleActressClick = (actress) => {
    window.location.href = `/search/actress?actress=${actress}`;
  }

  const handleVideoClick = (video) => {
    if (video.video_url) {
      if (video.video_url.endsWith(".m3u8") || video.video_url.endsWith(".mp4")) {
        window.open(`${api.address}/videoplayer?video_url=${video.video_url}`);
      } else {
        window.open(`${api.address}/redirect_to?url=${video.video_url}`);
      }
    } else {
      history.push(`/search/video?code=${video.code}`);
    }
  }

  const handleMagnetClick = (code) => {
    history.push(`/search/magnet?code=${code}`);
  }

  const renderActress = (actress) => {
    if (!actress) {
      return (
        <Button size="small" color="secondary" disabled>
          Unknown
        </Button>
      )
    } else if (actress.includes(",")) {
      return (
        <>
          <Button size="small" aria-haspopup="true" color="secondary" onClick={handleMultipleClick}>
            Expand
          </Button>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMultipleClose}
          >
            {actress.split(",").map((x, i) => {
              return <MenuItem key={i.toString()} onClick={() => handleActressClick(x.trim())}>{x.trim()}</MenuItem>
            })}
          </Menu>
        </>
      );
    } else {
      return (
        <Button size="small" color="secondary" onClick={() => handleActressClick(video.actress)}>
          {video.actress}
        </Button>
      );
    }
  }

  const handleImageError = (event) => {

  }

  return (
    <Card className={classes.root}>
      <CardActionArea onClick={() => handleVideoClick(video)}>
        <LazyLoad>
          <CardMedia
            component="img"
            className={classes.media}
            image={video.preview_img_url}
            onError={handleImageError}
          />
        </LazyLoad>
        <CardContent className={classes.content}>
          <Typography gutterBottom variant="h5" component="h2">
            {video.code}
            <Chip size="small" label={video.release_date} className={classes.date} />
          </Typography>
          <Typography variant="body2" component="p">
            {video.title}
          </Typography>
        </CardContent>

      </CardActionArea>

      <CardActions className={classes.bottom}>
        {renderActress(video.actress)}
        <Button size="small" color="secondary" onClick={() => handleMagnetClick(video.code)}>
          MAGNET
        </Button>
      </CardActions>
    </Card >
  );
}