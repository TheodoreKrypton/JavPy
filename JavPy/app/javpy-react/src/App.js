import React from 'react';
import New from './pages/New'
import './App.css';
import theme from './theme';
import { ThemeProvider } from '@material-ui/styles';
import {
  Switch,
  Route,
  Redirect
} from "react-router-dom";
import SearchVideo from './pages/SearchVideo';
import SearchActress from './pages/SearchActress';
import SearchMagnet from './pages/SearchMagnet';
import Login from './pages/Login';
import VideoPlayer from './pages/VideoPlayer';
import { withRouter } from 'react-router';
import PropTypes from 'prop-types';
import IFrame from './pages/IFrame';
import TopArea from './components/TopArea';

class App extends React.Component {
  static propTypes = {
    location: PropTypes.object.isRequired
  }

  componentDidUpdate(prevProps) {

  }

  render() {
    return (
      <Switch>
        <Route exact path="/videoplayer">
          <VideoPlayer></VideoPlayer>
        </Route>
        <Route exact path="/iframe">
          <IFrame></IFrame>
        </Route>
        <Route>
          <ThemeProvider theme={theme}>
            <div>
              <Login></Login>
              <TopArea></TopArea>
              <div style={{ position: "absolute", top: 70, width: "100%" }}>
                <Switch>
                  <Redirect exact path="/" to="/new" />
                  <Route path="/new">
                    <New></New>
                  </Route>
                  <Route path="/search/video">
                    <SearchVideo></SearchVideo>
                  </Route>
                  <Route path="/search/actress">
                    <SearchActress></SearchActress>
                  </Route>
                  <Route path="/search/magnet">
                    <SearchMagnet></SearchMagnet>
                  </Route>
                </Switch>
              </div>
            </div>
          </ThemeProvider >
        </Route>
      </Switch >
    );
  }
}

export default withRouter(App);
