import React from 'react';
import SearchBar from './components/SearchBar'
import New from './pages/New'
import './App.css';
import theme from './theme';
import { ThemeProvider } from '@material-ui/styles';
import {
  BrowserRouter,
  Switch,
  Route,
  Redirect
} from "react-router-dom";
import SearchVideo from './pages/SearchVideo';
import SearchActress from './pages/SearchActress';
import SearchMagnet from './pages/SearchMagnet';
import Login from './pages/Login';

class App extends React.Component {
  render() {
    return (
      <ThemeProvider theme={theme}>
        <div>
          <Login></Login>
          <SearchBar></SearchBar>
          <BrowserRouter>
            <div>
              <Switch>
                <Redirect exact path="/" to="/new" />
                <Route exact path="/new">
                  <New></New>
                </Route>
                <Route exact path="/search/video">
                  <SearchVideo></SearchVideo>
                </Route>
                <Route exact path="/search/actress">
                  <SearchActress></SearchActress>
                </Route>
                <Route exact path="/search/magnet">
                  <SearchMagnet></SearchMagnet>
                </Route>
              </Switch>
            </div>
          </BrowserRouter>
        </div>
      </ThemeProvider >
    );
  }
}

export default App;
