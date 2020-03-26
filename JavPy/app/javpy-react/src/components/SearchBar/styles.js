import { makeStyles } from '@material-ui/core/styles';


export default makeStyles(theme => ({
  root: {
    padding: '2px 4px',
    display: 'flex',
    alignItems: 'center',
    maxWidth: 400,
    margin: '8px',
    zIndex: "1",
    position: "sticky",
    top: "8px"
  },

  input: {
    marginLeft: theme.spacing(1),
    flex: 1,
  },

  iconButton: {
    padding: 10,
  },

  divider: {
    height: 28,
    margin: 4,
  },
}));
