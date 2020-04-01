import React from 'react'
import MenuItem from '@material-ui/core/MenuItem';
import Menu from '@material-ui/core/Menu';
import AccountCircle from '@material-ui/icons/AccountCircle';
import IconButton from '@material-ui/core/IconButton';


class Config extends React.Component {
  constructor(props) {
    super(props);
    this.state = { counter: 0 };
  }

  render() {
    const MenuDT = (
      <Menu
        anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
        id='config-dt'
        keepMounted
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
      >
        <MenuItem>Profile</MenuItem>
        <MenuItem>My account</MenuItem>
      </Menu>
    );

    const MenuMB = (
      <Menu
        anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
        id='config-mb'
        keepMounted
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
      >
        <MenuItem>
          <IconButton
            aria-label="account of current user"
            aria-controls="primary-search-account-menu"
            aria-haspopup="true"
            color="inherit"
          >
            <AccountCircle />
          </IconButton>
          <p>Profile</p>
        </MenuItem>
      </Menu>
    )

    return (
      <div>
        <MenuDT></MenuDT>
        <MenuMB></MenuMB>
      </div>
    )
  }
}
