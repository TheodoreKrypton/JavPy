import { makeStyles } from '@material-ui/core/styles';

export default makeStyles(theme => ({
  root: {
    left: 0,
    right: 0,
    margin: "auto",
    position: "relative",
    display: "flex",
    width: 400,
    maxWidth: "100vw",
    background: "#000000"
  },
  details: {
    display: 'flex',
    flexDirection: 'column',
  },
  content: {
    flex: '1 0 auto',
  },
  cover: {
    height: 200,
    width: "auto",
    maxWidth: "40vw",
    float: "right"
  },
}));