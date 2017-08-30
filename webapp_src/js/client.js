import React from 'react';
import ReactDom from 'react-dom';

import Main from './layouts/Main';
import Play from './pages/Play';
import Index from './pages/Index';

import {
  BrowserRouter as Router,
  Route,
  Link
} from 'react-router-dom';

const app = document.getElementById('app');

ReactDom.render(
  <Router>
    <Main>
      <Route exact path="/" component={Index} />
      <Route path="/play/:code" component={Play} />
    </Main>
  </Router>
  , app);
