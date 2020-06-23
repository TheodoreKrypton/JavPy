import React from 'react';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Typography from '@material-ui/core/Typography';
import useStyles from './styles';

const formatDate = (date) => {
  if (!date) {
    return ""
  }
  date = new Date(date);
  const ye = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(date)
  const mo = new Intl.DateTimeFormat('en', { month: 'numeric' }).format(date)
  const da = new Intl.DateTimeFormat('en', { day: '2-digit' }).format(date)
  return `${da}/${mo}/${ye}`
}


export default (props) => {
  const classes = useStyles();

  const { name, profile } = props;

  if (!profile) {
    return <></>
  }

  return (
    <Card className={classes.root}>
      <div className={classes.details}>
        <CardContent className={classes.content}>
          <Typography component="h5" variant="h5">
            {name}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            Birthdate: {formatDate(profile.birth_date)}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            Height: {profile.height}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            Weight: {profile.weight}
          </Typography>
        </CardContent>
      </div>
      <CardMedia
        component="img"
        className={classes.cover}
        image={profile.img}
      />
    </Card>
  );
}