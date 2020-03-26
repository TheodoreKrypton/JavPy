import { makeStyles } from '@material-ui/core/styles';

export default makeStyles({
  root: {
    width: 350,
    maxWidth: "80vw",
    margin: 8,
    height: 400,
    background: "rgba(255, 255, 255, 0.1)"
  },
  media: {
    height: 200,
  },
  content: {
    poadding: 8,
    height: 120,
    overflow: "hidden"
  },
  bottom: {
    position: "relative",
    height: 30,
  },
  date: {
    position: "absolute",
    right: 16
  }
});