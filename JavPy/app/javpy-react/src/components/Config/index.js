import React from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import IconButton from '@material-ui/core/IconButton';
import SettingsIcon from '@material-ui/icons/Settings';
import ReactJson from 'react-json-view'
import api from '../../api';

export default () => {
  const [open, setOpen] = React.useState(false);
  const [json, setJson] = React.useState(null);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleConfirm = () => {
    api.updateConfigurations(json).finally(() => {
      setOpen(false);
    })
  };

  React.useEffect(() => {
    api.getConfigurations().then((rsp) => {
      setJson(rsp)
    })
  }, [open])

  const edit = ({ updated_src, name, namespace, new_value, existing_value }) => {
    setJson(updated_src);
  }

  const add = ({ updated_src, name, namespace, new_value, existing_value }) => {
    setJson(updated_src);
  }

  const del = ({ updated_src, name, namespace, new_value, existing_value }) => {
    setJson(updated_src);
  }

  return (
    <div>
      <IconButton onClick={handleClickOpen}>
        <SettingsIcon></SettingsIcon>
      </IconButton>
      <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title" fullWidth>
        <DialogTitle id="form-dialog-title">Configurations</DialogTitle>
        <DialogContent>
          {json ? <ReactJson src={json} onEdit={edit} onDelete={del} onAdd={add} theme="solarized"></ReactJson> : <></>}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>
            Cancel
          </Button>
          <Button onClick={handleConfirm}>
            Confirm
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}