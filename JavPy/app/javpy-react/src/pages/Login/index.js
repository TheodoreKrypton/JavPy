import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import api from '../../api';

export default function FormDialog() {
  const [input, setInput] = React.useState("");
  const [open, setOpen] = React.useState(!api.hasUserpass());

  const handleProceed = () => {
    api.authByPassword({ password: input }).then((rsp) => {
      if (rsp) {
        setOpen(false);
        window.location.reload();
      }
    })
  };

  return (
    <React.Fragment>
      <Dialog open={open} onClose={handleProceed}>
        <DialogTitle>Login Required</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Leave it blank if you didn't set a password.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            label="password"
            type="password"
            color="secondary"
            value={input}
            onChange={event => { setInput(event.target.value); }}
            fullWidth
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleProceed} color="secondary">
            Proceed
          </Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
}