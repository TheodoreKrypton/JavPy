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
import VideoPlayer from './pages/VideoPlayer'

class App extends React.Component {
  render() {
    return (
      <BrowserRouter>
        <Switch>
          <Route exact path="/videoplayer">
            <VideoPlayer></VideoPlayer>
          </Route>
          <Route>
            <ThemeProvider theme={theme}>
              <div>
                <Login></Login>
                <SearchBar></SearchBar>
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
              </div>
            </ThemeProvider >
          </Route>
        </Switch>
      </BrowserRouter>
    );
  }
}

export default App;
