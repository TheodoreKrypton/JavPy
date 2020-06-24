import React from 'react';
import Config from '../Config';
import SearchBar from '../SearchBar';

export default () => {
  return (
    <React.Fragment>
      <table style={{ position: "fixed", top: 0, zIndex: 1 }}>
        <tbody>
          <tr>
            <td>
              <Config></Config>
            </td>
            <td>
              <SearchBar></SearchBar>
            </td>
          </tr>
        </tbody>
      </table>
    </React.Fragment>
  )
}